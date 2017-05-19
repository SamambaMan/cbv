def obrigar_cadastro_complementar(function):
    def wrap(request, *args, **kwargs):
        from django.shortcuts import redirect

        if request.user.is_anonymous():
            return function(request, *args, **kwargs)

        if request.user.is_authenticated() and \
           not request.user.infosadicionaisusuario.cadastrocompleto:
            return redirect('/cadastrocomplementar/')

        return function(request, *args, **kwargs)


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
