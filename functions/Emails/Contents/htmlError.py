from .htmlSignature import html_signature

# Generate HTML of errpr email
def html_error(error):
    return f"""
    <p>
        Hello Daniel,
    </p>
    <p>
        The following error occurred while sending the convention email:
    </p>
    <pre>
      <code>
        {error}
      </code>
    </pre>
    <p>
        Kind regards,
    </p>
    {html_signature()}
    """
