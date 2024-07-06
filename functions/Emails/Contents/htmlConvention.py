from .htmlSignature import html_signature

# Generate HTML of attestation email for teacher
def html_convention(params):
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
        La convention est attachée au lien qui suit.
        Merci de télécharger le document en format pdf, de le signer et de le renvoyer à travers le formulaire
        <a href="https://forms.gle/UNGTKerziGy4yTdh7">suivant</a>.
    </p>
    <p>
        Lien vers le document: <a href="{params.get('sharableLink')}">Cliquez ici</a>.
    </p>
    <p>
        Un tout grand merci pour le travail fourni ce mois et une belle journée,
    </p>
    <p>
        Bien à toi,
    </p>
    {html_signature()}
    """
