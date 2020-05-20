import math as ma


# Fonctions


def euclide(a, b):
    u, v = abs(a), abs(b)
    while v != 0:
        u, v = v, u % v
    return u


def ppcm(a, b):
    pgcd = euclide(a, b)

    return a * b / pgcd


def create_poly_w_deg(deg):
    coef = [Rational(0) for x in range(deg + 1)]
    coef[deg] = Rational(1)

    return Polynome(coef)


# Classes Rational


class Rational:
    numerator = 0  # p
    denominator = 1  # q

    def __init__(self, p, q=1):
        if q == 0:
            raise Exception("q doit être strictement positif")

        if q < 0:
            self.numerator = -p  # on reporte le signe de q sur p
            self.denominator = -q  # on prend q > 0
        else:
            self.numerator = p
            self.denominator = q

        self.simplify()

    def simplify(self):
        pgcd = euclide(self.denominator, self.numerator)

        self.denominator //= pgcd
        self.numerator //= pgcd

    # DEFINITION DES OPERATIONS #

    def __add__(self, other):  # Addition
        """
        Addition de deux rationnels ou un rationnel et entier (int)

        :param other:
        :return Rational: Le résultat
        """

        if type(other) == Rational:
            return Rational(self.numerator * other.denominator + other.numerator * self.denominator,
                            self.denominator * other.denominator)
        elif type(other) == int:
            return Rational(self.numerator + other * self.denominator,
                            self.denominator)
        else:
            return NotImplemented

    def __mul__(self, other):  # Multiplication
        """
        Multiplication de deux rationels ou un rationel et entier (int)
        :param other:
        :return Rational: Le résultat
        """

        if type(other) == Rational:
            return Rational(self.numerator * other.numerator,
                            self.denominator * other.denominator)
        elif type(other) == int:
            return Rational(self.numerator * other,
                            self.denominator)
        else:
            return NotImplemented

    def __truediv__(self, other):  # Division
        """
        Division de deux rationels ou un rationel et entier (int)
        :param other:
        :return Rational: Le résultat
        """

        if type(other) == Rational:
            return Rational(self.numerator * other.denominator,
                            self.denominator * other.numerator)
        elif type(other) == int:
            return Rational(self.numerator,
                            self.denominator * other)
        else:
            return NotImplemented

    def __neg__(self):  # Opposé
        """
        Opposé

        :return Rational: Le résultat
        """
        return Rational(-self.numerator, self.denominator)

    def __sub__(self, other):  # Soustraction. Définie à partir de l'addition et de l'opposé
        """
        Soustraction de deux rationels ou un rationel et entier (int)
        :param other:
        :return Rational: Le résultat
        """
        return self + (-other)

    def __pow__(self, power, modulo=None):  # Puissance
        """
        Puissance

        :return Rational: Le résultat
        """
        return Rational(self.numerator ** power, self.denominator ** power)

    # OPERATIONS A DROITE #

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rsub__(self, other):
        return -1 * self + other

    def __rtruediv__(self, other):
        return Rational(1) / self * other

    # COMPARAISONS #

    def __eq__(self, other):
        self.simplify()

        if type(other) == int:
            return self.denominator == 1 and self.numerator == other
        elif type(other) == Rational:
            other.simplify()
            return (self.numerator == 0 and other.numerator == 0) or (
                    self.numerator == other.numerator and self.denominator == other.denominator)
        else:
            return NotImplemented

    # CONVERTIR DANS D'AUTRE TYPE #

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return str(self.numerator) + "/" + str(self.denominator)

    def __int__(self):
        return int(self.numerator / self.denominator)

    def __float__(self):
        return float(self.numerator) / float(self.denominator)


class Polynome:  # un polynôme
    __coef__ = []

    def __init__(self, coef):
        """
        Créer un polynôme à partir de la liste de coefficient

        :param coef: Liste de Rationnel
        """
        k = len(coef) - 1  # dernier coefficient

        while coef[k] == Rational(0) and k > 0:  # pour avoir coefficient non nul de plus grand degré
            k -= 1

        if k < 0:  # si il n'y a que des coefficients nuls
            coef.append(Rational(0))  # polynôme nul
        else:
            self.__coef__ = coef[:k + 1]

    def deg(self):
        """
        Calcul le degré du polynôme

        :return: degré
        """
        k = len(self.__coef__) - 1  # plus grand coefficient

        while self.__coef__[k] == Rational(0) and k >= 0:  # pour avoir coefficient non nul de plus grand degré
            k -= 1

        if k < 0:
            return -ma.inf
        else:
            return k

    def coef(self, k):
        """
        Récupérer le k-ème coefficient du polynôme

        :param k:
        :return: le k-ème coefficient
        """

        if k > self.deg():  # si au dessus du degré alors coefficient = 0
            return Rational(0)
        else:
            return self.__coef__[k]  # si non on renvoie la case

    def c(self):
        """
        Coefficient dominant

        :return: le coefficient dominant
        """

        k = self.deg()
        if k >= 0:  # Si le degré est supérieur ou égal à zero (ie polynôme non nul)
            return self.coef(k)

    def transformer_en_unitaire(self):
        """
        Transformer le polynôme en polynôme unitaire (id coefficient dominant égal à 1)

        Attention : Remplace simplement le coefficient dominant

        :return: le coefficient dominant
        """

        k = self.deg()

        if k >= 0:
            self.__coef__[k] = Rational(1)

    # OPERATIONS #

    def __add__(self, other):
        """
        Addition de deux polynômes

        :param other:
        :return Polynome: self + other
        """

        if type(other) == Polynome:
            coef = []

            if self.deg() == -ma.inf:  # Si l'un est le polynomes nuls on renvoie l'autre
                coef = other.__coef__
            elif other.deg() == -ma.inf:  # et inversement
                coef = self.__coef__
            else:
                for k in range(max(self.deg(), other.deg()) + 1):  # on fait la somme de chaque coefficient
                    coef.append(self.coef(k) + other.coef(k))  # fonction 'coef' définie pour tout nombre positif

            return Polynome(coef)
        else:
            return NotImplemented

    def __mul__(self, other):
        """
        Multiplication de :
        - deux polynômes
        - polynôme et scalaire
        - polynôme et entier (int)

        :param other:
        :return Polynome: self * other
        """

        if type(other) == Polynome:  # Deux polynômes
            coef = []

            if self.deg() == -ma.inf or other.deg() == -ma.inf:  # Si l'un des deux est le polynomes nuls
                coef.append(Rational(0))
            else:
                for k in range(self.deg() + other.deg() + 1):  # coefficient n+m bien définie d'où +1
                    s = 0
                    for i in range(k + 1):  # Formule du produit
                        s += self.coef(i) * other.coef(k - i)
                    coef.append(s)

            return Polynome(coef)
        elif type(other) == Rational or type(other) == int:  # polynôme et scalaire ou polynôme et entier (int)
            coef = []

            if self.deg() == -ma.inf:  # Si l'un des deux est le polynomes nuls
                coef.append(Rational(0))
            else:
                for k in range(self.deg() + 1):
                    coef.append(self.coef(k) * other)

            return Polynome(coef)
        else:
            return NotImplemented

    def __truediv__(self, other):
        """
        Division polynôme par scalaire

        :param other:
        :return Polynome: self/other
        """

        if type(other) == Rational:
            return self * (1 / other)
        elif type(other) == int:
            return self * Rational(1, other)
        else:
            return NotImplemented

    def __neg__(self):
        """
        Opposé

        :return Rational: -self
        """
        return self.__mul__(-1)

    def __sub__(self, other):
        """
        Soustraction de deux polynômes

        :param other:
        :return Polynome: Le résultat
        """
        if type(other) == Polynome:
            return self + (-other)
        else:
            return NotImplemented

    # OPERATIONS A DROITE #

    # Comme l'addition, la soustraction n'existe qu'entre polynôme
    # et la division n'est pas définie à droite
    # il n'est pas nécessaire de définir ces opérations à droite

    def __rmul__(self, other):
        return self.__mul__(other)

    # DIVISION EUCLIDIENNE #

    def __division_euclide__(self, other):
        m = other.deg()

        q = Polynome([0])
        r = self

        while r.deg() >= m:
            q += create_poly_w_deg(r.deg() - m) * (r.c() / other.c())
            r = self - q * other

        return q, r

    def __floordiv__(self, other):
        """
        Quotient de la division euclidienne

        :param other:
        :return Polynome: Quotient
        """
        return self.__division_euclide__(other)[0]

    def __mod__(self, other):
        """
        Reste de la division euclidienne

        :param other:
        :return Polynome: Reste
        """
        return self.__division_euclide__(other)[1]

    # COMPARAISONS #

    def __eq__(self, other):
        if type(other) == Polynome:  # Doit être du même type
            if self.deg() == other.deg():  # Doit être du même degré
                for k in range(self.deg() + 1):  # Doit avoir les mêmes coefficients
                    if self.coef(k) != other.coef(k):
                        return False
                return True
            else:
                return False
        else:
            return False

    # CONVERSION #

    def __str__(self):
        """
        Formatage du polynôme avec une indéterminée X, pour un affichage plus lisible

        :return string: Polynôme sous forme d'une chaine caractère
        """
        r = ""
        if self.deg() == -ma.inf:
            r = "0"
        else:
            for k in range(self.deg(), 0, -1):
                r += str(self.coef(k)) + "X^" + str(k) + " + "

            r += str(self.coef(0))

        return r


# TESTS


A = Rational(2, 3)
B = Rational(9, 2)

print("Début Rationnal")
print(A + B)
print(B + A)

print(A * B)
print(B * A)

print(-A)
print(A ** 2)

print(A - B)
print(B - A)

print(A / B)
print(B / A)

print(A + 2)
print(2 + A)

print(A * 2)
print(2 * A)

print(A - 2)
print(2 - A)

print(A / 2)
print(2 / A)
print("Fin Rationnal")

P = Polynome([Rational(1), Rational(1), Rational(1), Rational(1)])
Q = Polynome([Rational(1), Rational(1), Rational(1), Rational(1), Rational(1), Rational(1)])

print("Début Polynome")
print("Addition")
print(P + Q)
print(Q + P)

print("Opposé")
print(-P)

print("Soustraction")
print(P - Q)
print(Q - P)

print("Multiplication")
print("interne")
print(P * Q)
print(Q * P)

print("avec int")
print(P * 2)
print(2 * P)

print("avec rationnel")
print(P * A)
print(A * P)

print("Division")
print("avec int")
print(P / 2)

print("avec rationnel")
print(P / A)

print("Quotient division Euclidienne")
print(P // Q)
print(Q // P)

print("Reste division Euclidienne")
print(P % Q)
print(Q % P)

print("Fin Polynome")


# Fonctions


def euclide_polynome(a, b):
    u, v = a, b
    while v.deg() >= 0:
        u, v = v, u % v

    u.transformer_en_unitaire()
    return u


def ppcm_polynome(a, b):
    pgcd = euclide_polynome(a, b)

    return a * b // pgcd


P = Polynome([Rational(1), Rational(1), Rational(1), Rational(1)])
Q = Polynome([Rational(1), Rational(1), Rational(1), Rational(1), Rational(1), Rational(1)])

S = Rational(0)
for i in range(1, 1011):
    S += Rational(1, (2*i-1)*(2*i+1))
print(S)
