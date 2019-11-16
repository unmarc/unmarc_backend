import graphene
from graphene_django import DjangoObjectType

from .models import Branch


class BranchType(DjangoObjectType):
    class Meta:
        model = Branch


class Query:
    all_branches = graphene.List(BranchType)

    def resolve_all_branches(self, info):
        return Branch.objects.all()
