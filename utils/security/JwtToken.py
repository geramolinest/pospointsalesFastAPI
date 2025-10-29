import jwt
import logging

from uuid import UUID
from datetime import datetime, timedelta, timezone
from utils import ConfigDep, Config
from application.dto.security import Token, GetUser

class JwtToken:
    
    __config: Config
    __secret_key: str | None
    __algorithm: str | None
    __expires_delta: str | None
    
    def __init__(self, config: ConfigDep) -> None:
        self.__config = config
        self.__algorithm = self.__config.get_value('ALGORITHM')
        self.__secret_key: str | None= self.__config.get_value('SECRET_KEY')
        self.__expires_delta: str | None = self.__config.get_value('ACCESS_TOKEN_EXPIRE_MINUTES')
    
    def create_access_token(self, payload: dict[str, str | int | datetime | UUID]) -> Token:
        
        if not self.__expires_delta or not self.__expires_delta.isnumeric():
            raise jwt.exceptions.PyJWTError('Expiration token not provided or it has an invalid format, check your env file')
        
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=int(self.__expires_delta))
        
        payload['exp'] = expire
        
        if not self.__secret_key:
            raise jwt.InvalidKeyError('Key not provided, check your env file')
 
        if not self.__algorithm:
            raise jwt.InvalidAlgorithmError('Not algorithm provided, check your env file')
        
        logging.info('Environment was loaded successfully, building token...')
        
        encoded_jwt: str = jwt.encode(payload, self.__secret_key, self.__algorithm)
        
        logging.info('Token builded successfully, building Token entity.')
        
        expiration_token: int = int(self.__expires_delta) * 60
        
        
        token: Token =  Token( access_token=encoded_jwt, expires_in=expiration_token)
        
        logging.info('Token entity builded successfully, returning Token entity as response from JwtToken utility.')
        
        return token
    
    def verify_token(self, token: str) -> GetUser | None:

        if not self.__secret_key:
            raise jwt.InvalidKeyError('Key not provided, check your env file')
 
        if not self.__algorithm:
            raise jwt.InvalidAlgorithmError('Not algorithm provided, check your env file')
        
        try:

            decoded_token: dict[str, str | datetime | int] = jwt.decode(token, self.__secret_key, self.__algorithm)

            user_from_decoded_token: GetUser = GetUser( **decoded_token ) # type: ignore

            return user_from_decoded_token
        except Exception as e:
            logging.error(e)
            return None