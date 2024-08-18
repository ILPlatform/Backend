# These functions are related to the management of the documents. Documents may be Attestations, Contracts, Payslips, etc.

# Admin functions
from .Docs_A_Create import docs_A_create
from .Docs_A_Delete import docs_A_delete
from .Docs_A_GetAll import docs_A_get_all

# User functions
from .Docs_U_Get import docs_U_get
from .Docs_U_UpdateSigned import docs_U_update_signed
