from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or view it through api
    """

    def has_object_permission(self, request, view, obj):
        #Allow access only if objec'ts owner is the same as the user making the request
        print "tsekkaa luvat"

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user