from dj_rest_auth.serializers import UserDetailsSerializer


class UserDetailSerializer(UserDetailsSerializer):
    """
    UserSerializer를 확장하여 소셜 계정 정보를 포함
    """

    class Meta(UserDetailsSerializer.Meta):
        fields = tuple(f for f in UserDetailsSerializer.Meta.fields if f != "pk") + (
            "id",
            "username",
        )

        read_only_fields = tuple(
            f for f in UserDetailsSerializer.Meta.read_only_fields if f != "pk"
        ) + (
            "id",
            "username",
        )
