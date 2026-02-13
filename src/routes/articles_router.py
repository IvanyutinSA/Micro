router = APIRouter(prefix="/users")


@router.post("/")
def register(request: CreateUserRequest) -> CreateUserReply:
    return register_user(request)


@router.post("/login")
def authenticate(request: Annotated[OAuth2PasswordRequestForm, Depends()]
                 ) -> Token:
    return authenticate_user(request)


@router.get("/")
def get_current_user(request: Annotated[GetUserReply,
                                        Depends(get_current_user_req)]
                     ) -> GetUserReply:
    return get_user(request)


@router.put("/")
def update_current_user(request: UpdateCurrentUserRequest,
                        get_user_req: Annotated[GetUserReply,
                                                Depends(get_current_user_req)]
                        ) -> UpdateUserReply:
    request = UpdateUserRequest(username=get_user_req.username,
                                password=request.password,
                                email=request.email,
                                image_url=request.image_url,
                                bio=request.bio)
    return update_user(request)
