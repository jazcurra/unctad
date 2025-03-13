import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    files = [
        # Make the file available in local system working directory
        client.files.upload(file="Mapping Project Description and Methodology.pdf"),
        # Make the file available in local system working directory
        client.files.upload(file="1.pdf"),
    ]
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_uri(
                    file_uri=files[1].uri,
                    mime_type=files[1].mime_type,
                ),
                types.Part.from_text(text="""Using the Mapping Project Description instructions, analyze the BIT and show the result as a table until the page 
26"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Okay, I will analyze the treaty extracts provided, using the UNCTAD IIA Mapping Project definitions, and present the results in a table.

**Disclaimer:** Based on the limited extract, this analysis may be incomplete. A full treaty text is required for an accurate mapping. Also I cannot insert a table as requested. I can only create an analysis.

**Analysis of the Germany-Afghanistan BIT (2005) based on UNCTAD IIA Mapping Project Definitions**

Here's the breakdown based on the provided document. Due to the limitations of the text provided, some sections will be marked as \"Inconclusive\" or \"Not Applicable\"

| Section                           | Question                                                                   | Answer       | Notes                                                                                                                                                                                                  |
| :-------------------------------- | :------------------------------------------------------------------------- | :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Preamble**                     | Reference to right to regulate?                                         | Inconclusive  | Preamble text is incomplete in the given document.                                                                                                                                                       |
|                                   | Reference to sustainable development?                                      | No           | The text doesn't show a mention to sustainability matters.                                                                                                                                                  |
|                                   | Reference to social investment aspects?                                   | No           | The text doesn't show a mention to social aspects.                                                                                                                                                      |
|                                   | Reference to environmental aspects?                                      | No           | The text doesn't show a mention to environment matters.                                                                                                                                                      |
| **Scope and Definitions**          | Definition of Investment: Type                                              | Asset-based  | Article 1 defines \"investments\" as encompassing \"every kind of asset,\" followed by an illustrative list.                                                                                                   |
|                                   | Definition of Investment: Excludes portfolio investment?                       | No           | The text does not show an exclusion of portfolio investments.                                                                                                                                                  |
|                                   | Definition of Investment: Excludes other specific assets?                    | No           | The text does not show an exclusion of specific assets.                                                                                                                                                    |
|                                   | Definition of Investment: Lists required characteristics of investment?       | No           | The text does not show listing of certain investment traits.                                                                                                                                           |
|                                   | Definition of Investment: Contains \"in accordance with host State laws\" requirement? | No           | There are no evidence of \"in accordance with Host State laws\" requirement.                                                                                                                                             |
|                                   | Definition of Investment: Sets out closed list of covered assets?              | No           | The definition in Article 1 is illustrative and open-ended.                                                                                                                                            |
|                                   | Definition of Investor: Definition included?                                | Yes          | Article 1 defines \"investor\" for both Germany and Afghanistan.                                                                                                                                       |
|                                   | Specifying natural persons covered: Includes permanent residents?              | No           | The definition focuses on \"nationals/citizens\" based on the Basic Law/Constitution, not permanent residents.                                                                                           |
|                                   | Specifying natural persons covered: Excludes dual nationals?                  | No           | The text doesn´t show exclusion of dual nationals                                                                                                                                                 |
|                                   | Includes requirement of substantial business activity?                        | No           | No requirement of substantial business activity can be deducted.                                                                                                                                                    |
|                                   | Defines ownership and control of legal entities?                            | No           | There is not defined ownership and control of legal entities                                                                                                                                           |
| **Denial of Benefits (DoB)**     | DoB clause included?                                                      | No  | The current treaty fragment provides no DoB Clause |
| **Substantive Scope of Treaty**  | Excludes taxation?                                                         | No           | No taxation exclusion can be inferred from the provided text.                                                                                                                                         |
|                                   | Excludes subsidies, grants?                                                  | No           | The text does not show mention of exclusion.                                                                                                                                                     |
|                                   | Excludes government procurement?                                             | No           | The text does not show mention of exclusion.                                                                                                                                                     |
|                                   | Excludes other subject matter?                                                | No           | The text does not show mention of exclusion.                                                                                                                                                     |
| **Temporal Scope of Treaty**       | Investments covered: Applies to post-BIT investments only?                      | No           | Article 9 states that the treaty applies to investments made *before* entry into force.                                                                                                                 |
|                                   | Investments covered: Applies to both pre-existing and post-BIT investments?    | Yes          | Based on Article 9.                                                                                                                                                                                  |
|                                   | Disputes covered: Carves out pre-existing disputes?                            | Inconclusive  | The text does not indicate that they can be deducted.                                                                                                                                             |
| **Standards of Treatment**       | National Treatment (NT): Type of NT clause                                   | Inconclusive  | The Treaty provides for National Treatment.                                                                                                                                                  |
|                                   | NT: Reference to \"like circumstances\" (or similar)?                           | No           | No \"like circumstances\" clause detected in provided text.                                                                                                                                          |
|                                   | Most-Favored-Nation (MFN) Treatment: Type of MFN clause                      | Inconclusive  | The Treaty provides for Most-Favored-Nation treatment.                                                                                                                                              |
|                                   | Exceptions from MFN obligation: Economic integration agreements?             | Yes          | Article 3(3) excludes privileges granted due to membership in customs/economic unions.                                                                                                              |
|                                   | Exceptions from MFN obligation: Taxation treaties?                           | Yes          | Article 3(4) excludes advantages derived from double taxation agreements.                                                                                                                            |
|                                   | Exceptions from MFN obligation: Procedural issues (ISDS)                       | No  | The current treaty fragment provides no exclusion of ISDS |
|                                   | Fair and Equitable Treatment (FET): Type of FET clause                        | Inconclusive  | The treaty provides for fair and equitable treatment, but the given portion of the text is not enough to classify whether it is qualified or unqualified.                                           |
|                                   | Full Protection and Security: Standard?                                       | Yes          | Article 4(1) provides for \"full protection and security.\"                                                                                                                                           |
|                                   | Full Protection and Security: With reference to domestic law?                  | No           | No reference to domestic law.                                                                                                                                                                 |
|                                   | Prohibition on unreasonable, arbitrary, or discriminatory measures?            | Yes          | Article 2(3) prohibits \"arbitrary or discriminatory measures\".                                                                                                                                      |
| **Expropriation**                   | Scope of measures covered: Indirect expropriation not mentioned?               | No           | Article 4(2) prohibits measures \"tantamount to expropriation.\"                                                                                                                                       |
|                                   | Indirect expropriation defined?                                               | No           | No definition of indirect expropriation in this extract.                                                                                                                                                  |
|                                   | Carve-out for general regulatory measures?                                   | Inconclusive  | Article 3 provides certain flexibility.  But more treaty text is needed for a clear conclusion                                                                                                  |
|                                   | Carve-out for compulsory licenses in conformity with WTO?                      | No           | Not mentioned                                                                                                                                                                                        |
| **Protection from Strife**         | Specifications: Relative right to compensation (comparator)                   | MFN and NT  | Article 4(3) provides treatment no less favorable than own investors regarding restitution, compensation of losses.   |
|                                   | Absolute right to compensation in certain circumstances?                    | No           | No absolute right to compensation, relative treatment is provided.                                                                                                                                   |
| **Transfer of Funds**              | Includes transfer of funds?                                                  | Yes          | Article 5 guarantees the free transfer of payments related to an investment.                                                                                                                           |
|                                   | Exceptions to transfer of funds obligation: Balance-of-payments exception?    | No  | There are no evidence of this exemption.                                                                                                                                                  |
| **Prohibition of Performance Requirements (PRs)** | Includes prohibition of PRs                                      | No  | No Explicit PRs clause|
| **Umbrella Clause**                | Umbrella clause?                                                              | No |There is no Umbrella clause.|
| **Transparency** | Directed at States (obligation to publish laws and regulations) |No| No indications about obligations to states|
|                                   | Directed at investors	 |No | No indications about obligations to states|
| **Health and Environment**        | Health and environment (any mentioning in the text, except preamble)?        | No | No reference in this section|
| **Labour Standards**        | Labour standards (any mentioning in the text, except preamble)?       | No  |  No reference in this section |
| **Right to regulate**        | Right to regulate (any mentioning in the text of this or similar concepts, except preamble)?       | No  |  No reference in this section |
| **Corruption**        | Corruption (any mentioning in the text, except preamble)?       | No   |  No reference in this section|
| **Not lowering of standards**        | Not lowering of standards (typically environment and/or labour standards) | No   |  No reference in this section|
| **Subrogation clause**        | Subrogation clause	 |Yes  | Article 6|
| **Investment promotion**        | Investment promotion	 | No   |   No mention in this section|
| **Exceptions**       | Exception included	 |Inconclusive | Article 3 provides certain flexibility. But more treaty text is needed for a clear conclusion |
| **SSDS**       | SSDS included	 |Yes  | Article 10 |
| **ISDS**       | ISDS included	 |Yes  | Article 11 |
| **ISDS**       | Limitation period for submission of claims | No  | There are no evidence of this exemption |
|**Treaty Duration, Amendment and Termination**       |Includes modalities for unilateral termination  	 |No  |  |
|**Treaty Duration, Amendment and Termination**       |Includes modalities for amendment or renegotiation	 |No   | |
|**Treaty Duration, Amendment and Termination**       |\"Survival\"/\"sunset\" clause length	 |Yes  | Art. 14 (3): 20 years|

**Note:**  This is a preliminary analysis, and further scrutiny of the full text would be necessary for a definitive mapping.
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_CIVIC_INTEGRITY",
                threshold="BLOCK_LOW_AND_ABOVE",  # Block most
            ),
        ],
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Act as a lawyer experimented in analyzing Bilateral Investment Treaties. For that you use the Mapping definition contained in the pdf. The outcome of the analysis is create a table with 6 sections answering all the questions with Yes, No, Inconclusive and Not Applicable"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
