from .htmlSignature import html_signature

# Generate HTML of attestation email for teacher
def html_attestation_teacher(params):
    return f"""
    <p>
        Bonjour {params.get('name')},
    </p>
    <p>
        Ceci est un message automatique, issu d'un programme destiné à créer vos
        conventions et attestations (pour les bénévoles), et contrats et prestations (pour les employés).
        Comme aucun programme n'est parfait, et qu'il est encore en phase beta, n'hésitez
        pas à soumettre du feedback si vous observez un programme quelconque, que ce
        soit avec la création de vos attestations ou avec la procédure en général.
    </p>
    <p>
        Les prestations / l'attestation de {params.get('month')} {params.get('year')} sont disponibles sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents". Tu y retrouveras un bouton "Sign", qui te permets de téléverser la version signée de ton document. Pourvu que ce document nous parvient au plus tard le 6 {params.get('nextMonth')} {params.get('nextYear')}, le paiement sera traité avant le 9 {params.get('nextMonth')} {params.get('nextYear')}.
        Si le document nous parvient après cette date, le paiement risque d'être effectué avec les paiements du mois suivant.
    </p>
    <p>
        Un tout grand merci pour le travail fourni ce mois et une belle journée,
    </p>
    <p>
        Bien à toi,
    </p>
    {html_signature()}
    """

# Generate HTML of attestation email for admin
def html_attestation_admin(params):
    return f"""
    <p>
        Hello Daniel,
    </p>
    <p>
        I hope you are doing well! Don't forget to take breaks and relax, and give my bests to Ana!
    </p>
    <p>
        Attestations and Prestation Sheets have been created for {params.get('year')}-{params.get('month')} and
        sent to all the teachers. The documents are in the respective Google Drive folders,
        and the amounts have been updated in the Google Sheets. Here is a copy of all the data
        of the classes this month:
    </p>
    <pre>{params.get('admin_mail')}</pre>
    <p>
        As a reminder, the upload form may be found here: <a href="https://forms.gle/fnR8YSwZY8LtDq3z9">https://forms.gle/fnR8YSwZY8LtDq3z9</a>.
    </p>
    <p>
        Have a nice day and best regards,
    </p>
    {html_signature()}
    """
