# utils/contract_generator.py

def generate_contract(template_name, contract_details):
    """Generates a contract based on a template and provided details.
    This is a simplified example. Consider using a templating engine
    like Jinja2 for more complex contracts."""

    if template_name == "Standard Agreement":
      return f"""
      STANDARD AGREEMENT
      This agreement is made as of {contract_details.get('date', 'DATE')},
      between {contract_details.get('party1', 'PARTY1')} and {contract_details.get('party2', 'PARTY2')}.

      [Placeholder for further clauses]
      """
    elif template_name == "NDA":
      return f"""
      NON-DISCLOSURE AGREEMENT (NDA)

      This NDA is entered into as of [DATE], by and between
      {contract_details.get('disclosing_party', 'DISCLOSING_PARTY')}, and
      {contract_details.get('receiving_party', 'RECEIVING_PARTY')}.

      [Placeholder for confidential information definition, obligations, etc.]
      """

    else:
      return "Contract template not found."

if __name__ == "__main__":
    details = {"party1": "Acme Corp", "party2": "Beta Inc", "date": "2023-11-05"}
    contract = generate_contract("Standard Agreement", details)
    print(contract)