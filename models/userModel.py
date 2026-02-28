from pydantic import BaseModel, EmailStr, Field, field_validator


class User(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=10)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        special_chars = set("@$!%*?&")

        if len(value) < 10:
            raise ValueError("Password deve conter pelo menos 10 caracteres")
        if not any(c.islower() for c in value):
            raise ValueError("Password deve conter pelo menos uma letra minúscula")
        if not any(c.isupper() for c in value):
            raise ValueError("Password deve conter pelo menos uma letra maiúscula")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password deve conter pelo menos um dígito ")
        if not any(c in special_chars for c in value):
            raise ValueError("Password deve conter pelo menos um caractere especial: @$!%*?&")
        if not all(c.isalnum() or c in special_chars for c in value):
            raise ValueError("Password contém caracteres inválidos")

        return value
