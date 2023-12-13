from rest_framework.routers import DefaultRouter


class MyCustomRouter(DefaultRouter):
    """
    Router class that disables the PUT method.
    """
    def get_method_map(self, viewset, method_map):

        bound_methods = super().get_method_map(viewset, method_map)
        returned_methods = bound_methods
        #print("estou aqui nos métodos: ", bound_methods)
        if 'put' in bound_methods.keys():
            del bound_methods['put']
            returned_methods = bound_methods

        for chave, valor in list(bound_methods.items()):
            if valor=='set_password':
                bound_methods.pop(chave)
            if valor=='resend_activation':
                bound_methods.pop(chave)
            if valor=='activation':
                bound_methods.pop(chave)
            if valor=='reset_username':
                bound_methods.pop(chave)
            if valor=='reset_username_confirm':
                bound_methods.pop(chave)
            if valor=='set_username':
                bound_methods.pop(chave)
            if valor=='create':
                bound_methods.pop(chave)
            if valor=='list':
                bound_methods.pop(chave)
            if valor=='retrieve':
                bound_methods.pop(chave)
        print(bound_methods)
        return bound_methods