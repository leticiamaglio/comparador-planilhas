from legacy.perfis.generico import (
    transformar as transformar_generico
)

from legacy.perfis.notas_fiscais import (
    transformar as transformar_notas
)


PERFIS = {

    "Genérico": transformar_generico,

    "Reconciliação de Notas": transformar_notas

}


def aplicar_perfil(

    perfil,

    df_a,

    df_b

):

    return PERFIS[perfil](

        df_a,

        df_b

    )