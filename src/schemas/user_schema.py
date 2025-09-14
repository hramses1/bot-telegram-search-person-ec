from enum import Enum
from typing import Optional, Union
from datetime import datetime

from pydantic import (
    BaseModel,
    ValidationError,
    EmailStr,
    Field,
    AliasChoices,
    ConfigDict,
)

# ---- Enum del plan ----
class AccountPlan(str, Enum):
    FREE = "cbbhqmwd0n978pi"

# ---- Schemas ----
class UserSchema(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        extra="ignore",
    )

    id: str
    username: Optional[str] = "generic_username"
    email: Optional[EmailStr] = None
    emailVisibility: bool = True

    password: Optional[str] = "generic_password"
    passwordConfirm: Optional[str] = "generic_password"

    disable: bool = Field(default=False, validation_alias=AliasChoices("disabled", "disable"))

    name: Optional[str] = None
    plan: AccountPlan = AccountPlan.FREE
    number_requests: int = 0
    token: Optional[str] = "token_initial"


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        extra="ignore",
    )

    collectionId: str
    collectionName: str
    created: datetime
    updated: datetime = Field(validation_alias=AliasChoices("updated", "update"))
    disable: bool = Field(validation_alias=AliasChoices("disabled", "disable"))
    email: Optional[EmailStr] = None
    emailVisibility: bool
    id: str
    name: Optional[str] = None
    number_requests: int
    plan: AccountPlan
    username: str
    verified: bool


# ---- Handler de registro ----
def handle_register_user(result: Union[str, dict, bytes]):
    
    if isinstance(result, str) and result.strip():
        return "⚠️ Ya estás registrado. Bienvenido!"

    try:
        if isinstance(result, (str, bytes)):
            _ = UserResponseSchema.model_validate_json(result)
        else:
            _ = UserResponseSchema.model_validate(result)

    except ValidationError as e:
        return "⚠️ Ya estabas registrado (o respuesta inválida del servidor)."

    return "✅ Registro exitoso."
