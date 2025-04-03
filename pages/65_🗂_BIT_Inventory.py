import streamlit as st
import boto3
from pymongo import MongoClient
import pandas as pd
from urllib.parse import urlparse

# --- MongoDB Configuration ---
MONGO_URI = st.secrets.get("MONGO_URI")  # Store your MongoDB connection string in Streamlit secrets
DB_NAME = "itc"
COLLECTION_NAME = "bit"

# --- S3 Configuration ---
S3_BUCKET_URL = "s3://bit-documents/iia-pdf/"
ITEMS_PER_PAGE = 100


def is_valid_s3_url(url):
    """Checks if the given string is a valid s3:// URL."""
    try:
        parsed_url = urlparse(url)
        return parsed_url.scheme == "s3" and parsed_url.netloc
    except:
        return False

def get_bucket_name_from_url(s3_url):
    """Extracts the bucket name from an s3:// URL."""
    parsed_url = urlparse(s3_url)
    return parsed_url.netloc

@st.cache_resource
def get_mongo_client(uri):
    """Connects to MongoDB and returns the client."""
    client = MongoClient(
        uri,
        ssl= True,
        tlsAllowInvalidCertificates=True  # Disable certificate validation (use cautiously)
    )
    return client

@st.cache_data(ttl=3600)
def fetch_document_count(mongo_uri, db_name, collection_name):
    """Fetches the total count of documents in the collection."""
    client = get_mongo_client(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    count = collection.count_documents({})
    return count

@st.cache_data(ttl=3600)
def fetch_document_batch(mongo_uri, db_name, collection_name, page_number, items_per_page):
    """Fetches a batch of document data from MongoDB with projection and sort."""
    client = get_mongo_client(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    skip = (page_number - 1) * items_per_page
    projection = {"id": 1, "instrument": 1, "about": 1, "url": 1}
    sort_criteria = [("instrument", 1)]
    documents = list(collection.find({}, projection=projection, sort=sort_criteria).skip(skip).limit(items_per_page))
    print(f"Fetched {len(documents)} documents from page {page_number}.")
    return documents

def main():
    st.title("Document Browser")

    if not MONGO_URI:
        st.error("MongoDB connection URI not found in Streamlit secrets. Please configure it.")
        return

    if not S3_BUCKET_URL:
        st.warning("Please enter the public S3 bucket URL.")
        return

    if not is_valid_s3_url(S3_BUCKET_URL):
        st.error("Invalid S3 URL format. Please use 's3://bucket-name'.")
        return

    bucket_name = get_bucket_name_from_url(S3_BUCKET_URL)
    base_s3_url = f"https://{bucket_name}.s3.amazonaws.com/iia-pdf/"

    with st.spinner("Fetching document count..."):
        total_documents = fetch_document_count(MONGO_URI, DB_NAME, COLLECTION_NAME)

    if total_documents > 0:
        num_pages = (total_documents + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        current_page = st.sidebar.number_input("Page:", min_value=1, max_value=num_pages, value=1)

        with st.spinner(f"Fetching page {current_page} of documents..."):
            document_data = fetch_document_batch(MONGO_URI, DB_NAME, COLLECTION_NAME, current_page, ITEMS_PER_PAGE)

        if document_data:
            data = []
            for doc in document_data:
                filename = doc.get("id")
                url = doc.get("url", "N/A")
                description = doc.get("about", "No description available")
                instrument = doc.get("instrument", "N/A")
                if filename:
                    download_url = base_s3_url + str(filename) + ".pdf"
                    data.append({"Instrument": instrument,  "Source": f"[Link]({url})", "Download": f"[Download]({download_url})"})

            if data:
                df = pd.DataFrame(data)

                query = st.text_input("Search documents:", "")
                if query:
                    df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

                st.subheader(f"Documents (Page {current_page} of {num_pages})")
                st.markdown(df.to_markdown(index=False, numalign="left", stralign="left"), unsafe_allow_html=True)
            else:
                st.info(f"No documents found on page {current_page}.")
        else:
            st.error("Failed to fetch document data from MongoDB.")
    elif total_documents == 0:
        st.info("No documents found in the MongoDB collection.")
    else:
        st.error("Failed to fetch document count from MongoDB.")

if __name__ == "__main__":
    main()