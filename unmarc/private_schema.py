import graphene

from users import schema as users_schema
from library import schema as library_schema


class Query(users_schema.Query,
            library_schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
