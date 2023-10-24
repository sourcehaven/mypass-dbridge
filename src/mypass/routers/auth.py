from fastapi import APIRouter, status
from datetime import datetime, timedelta
from loguru import logger
from mypass.types.const import IDENTITY_UID, IDENTITY_USER

router = APIRouter(prefix='/auth')


@router.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration():
    request_json = request.json
    user = db_utils.insert_user(**request_json)
    token = user.token
    logger.debug(f'Registering user with identity:\n    {request_json["username"]}')
    tokens = {'token': token}
    return tokens, 201


@router.post('/login', status_code=status.HTTP_201_CREATED)
def login():
    request_json = request.json
    ref_token = request_json.pop('refresh_token', None)
    username = request_json['username']
    password = request_json['password']
    user = db_utils.get_user_login(username=username, password=password)
    user = user.unlock(password)
    token = user.token
    uid = user.id
    identity = {IDENTITY_UID: uid, IDENTITY_USER: username}
    logger.debug(f'Logging in with identity:\n    {identity["username"]}')
    # already logged-in users can request new fresh tokens
    # while also invalidating their old refresh tokens
    if ref_token is not None:
        # noinspection PyBroadException
        try:
            ref_jwt = decode_token(ref_token)
            ref_jti = ref_jwt['jti']
            ref_exp_dt = datetime.fromtimestamp(ref_jwt['exp'])
            db_utils.revoke_token(jti=ref_jti, exp_dt=ref_exp_dt)
            logger.debug(f'Revoked token with id: {ref_jti}')
        # invalid token error
        except Exception:
            pass
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)
    tokens = {'access_token': access_token, 'refresh_token': refresh_token}
    resp = make_response(tokens, 201)
    resp.set_cookie('username', user.username or '')
    resp.set_cookie('email', user.email or '')
    resp.set_cookie('firstname', user.firstname or '')
    resp.set_cookie('lastname', user.lastname or '')
    return resp


@router.get('/login', status_code=status.HTTP_204_NO_CONTENT)
def get_login():
    return ''


@router.post('/refresh', status_code=status.HTTP_201_CREATED)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    jwt = get_jwt()
    jti = jwt['jti']
    exp_dt = datetime.fromtimestamp(jwt['exp'])
    refresh_token = request.authorization.token
    # if near expiration return new refresh token
    if exp_dt - datetime.now() <= timedelta(days=1):
        refresh_token = create_refresh_token(identity=identity)
        db_utils.revoke_token(jti=jti, exp_dt=exp_dt)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@router.delete('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout():
    logger.debug('Logging out user.')
    jwt = get_jwt()
    jti = jwt['jti']
    exp_dt = datetime.fromtimestamp(jwt['exp'])
    db_utils.revoke_token(jti=jti, exp_dt=exp_dt)
    logger.debug(f'{jwt["type"].title()} token {jti} has been successfully blacklisted.')
    return ''
