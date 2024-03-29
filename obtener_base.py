from sympy import symbols, Poly, lcm, degree, LM, diff, simplify
from itertools import combinations

#Definir las variables
x, y, a, b = symbols('x y a b')

def spoly(f,g,ordering, selected_domain):
    '''Funcion que devuelve el S-polinomio dados dos polinomios y un orden monomial
       Args:
        - f: Primer polinomio
        - g: Segundo polinomio
        - ordering: Orden monomial deseado'''
    poly_f = Poly(f, domain=selected_domain) if f != 0 else 0
    poly_g = Poly(g, domain=selected_domain) if g != 0 else 0

    lm_f = poly_f.LM(order=ordering).as_expr()
    lm_g = poly_g.LM(order=ordering).as_expr()

    lcm_result = lcm(lm_f, lm_g)

    spoly = (((lcm_result / (poly_f.LT(order=ordering)[0].as_expr()) * \
        poly_g.LC(order=ordering)) ) * poly_f.as_expr()) \
            - ((  (lcm_result / (poly_g.LT(order=ordering)[0].as_expr())) \
                * poly_f.LC(order=ordering) ) * poly_g.as_expr())

    return simplify(spoly)

def NF_Butcher(f, G, ordering, selected_domain):
    '''Funcion que devuelve una forma normal usando NFBuchberger'''
    h = Poly(f, domain=selected_domain) if f != 0 else 0
    T = G.copy()


    while(h != 0):
        Gh = [g for g in T if lcm(LM(g, order=ordering), \
            LM(h, order=ordering)) == LM(h, order=ordering)]

        if not Gh:
            break

        g = Gh[0]
        Gh.remove(g)
        h = spoly(h,g, ordering, selected_domain)

    return h

def get_standart_base(domain, ordering, G, NF_func, spoly_func):
    '''Función que devuelve una base estándar
       Args:
       - selected_domain: Dominio de los coeficientes de nuestro polinomio
       - ordering: orden monomial deseado
       - G: nuestro conjunto finito G contenido en domain
       - NF_func: funcion que nos devuelve una forma normal débil
       - spoly_func: funcion que nos devuelve el s-polinomio dados dos polinomios'''

    S = G.copy()
    P = [(f,g) for f,g in combinations(S,2)] #Nuestra lista de pares

    while (len(P) != 0):
        f,g = P[0]
        P.remove((f,g))
        s_polinomio = spoly_func(f,g, ordering, domain)

        h = NF_func(s_polinomio, S, ordering, domain)
        if(type(h) != int):
            h = h.as_expr()

        if h != 0:
            for f in S:
                P.append((h,f))
            S.append(h)
    return S





#-----------------------------------------------
def Tjurina_generator(f, selected_domain):
    '''Funcion que devuelve el ideal de Tjurina
    Args:
        - f: Polinomio sobre el que queremos obtener el generador
        - selected_domain: Domain de Sympy del poliniomio'''

    poly_f = Poly(f, domain=selected_domain) if f != 0 else 0

    result = [] #Lista que devolveremos

    result.append(f)

    diff_x = diff(poly_f,x).as_expr()
    diff_y = diff(poly_f,y).as_expr()

    result.append(diff_x)
    result.append(diff_y)

    return result
#-----------------------------------------------
# PROGRAMA PRINCIPAL


selected_domain = 'CC' #Nuestro dominio son los complejos, C[x,y]
f = y**5 - x**7 + a*x**3*y**3 + b*x**4*y**4
ordering = 'grevlex'

tjurina = Tjurina_generator(f, selected_domain)

# Pasamos a obtener nuestra base estándar
base = get_standart_base(selected_domain,ordering,tjurina,NF_Butcher,spoly)

print(base)
