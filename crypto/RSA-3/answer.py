# Code for wiener attack taken from https://github.com/orisano/owiener/blob/master/owiener.py
from typing import Tuple, Iterator, Iterable, Optional


def isqrt(n: int) -> int:
    """
    ref: https://en.wikipedia.org/wiki/Integer_square_root
    
    >>> isqrt(289)
    17
    >>> isqrt(2)
    1
    >>> isqrt(1000000 ** 2)
    1000000
    """
    if n == 0:
        return 0

    # ref: https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Rough_estimation
    x = 2 ** ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def is_perfect_square(n: int) -> bool:
    """
    ref: https://hnw.hatenablog.com/entry/20140503
    >>> is_perfect_square(100)
    True
    
    >>> is_perfect_square(2000000000000000000000000000 ** 2)
    True
    >>> is_perfect_square(2000000000000000000000000000 ** 2 + 1)
    False
    """
    sq_mod256 = (1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
    if sq_mod256[n & 0xff] == 0:
        return False

    mt = (
        (9, (1,1,0,0,1,0,0,1,0)),
        (5, (1,1,0,0,1)),
        (7, (1,1,1,0,1,0,0)),
        (13, (1,1,0,1,1,0,0,0,0,1,1,0,1)),
        (17, (1,1,1,0,1,0,0,0,1,1,0,0,0,1,0,1,1))
    )
    a = n % (9 * 5 * 7 * 13 * 17)
    if any(t[a % m] == 0 for m, t in mt):
        return False

    return isqrt(n) ** 2 == n


def rational_to_contfrac(x: int, y: int) -> Iterator[int]:
    """
    ref: https://en.wikipedia.org/wiki/Euclidean_algorithm#Continued_fractions
    
    >>> list(rational_to_contfrac(4, 11))
    [0, 2, 1, 3]
    """
    while y:
        a = x // y
        yield a
        x, y = y, x - a * y


def contfrac_to_rational_iter(contfrac: Iterable[int]) -> Iterator[Tuple[int, int]]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf (6)
    """
    n0, d0 = 0, 1
    n1, d1 = 1, 0
    for q in contfrac:
        n = q * n1 + n0
        d = q * d1 + d0
        yield n, d
        n0, d0 = n1, d1
        n1, d1 = n, d


def convergents_from_contfrac(contfrac: Iterable[int]) -> Iterator[Tuple[int, int]]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf Section.3
    """
    n_, d_ = 1, 0
    for i, (n, d) in enumerate(contfrac_to_rational_iter(contfrac)):
        if i % 2 == 0:
            yield n + n_, d + d_
        else:
            yield n, d
        n_, d_ = n, d


def attack(e: int, n: int) -> Optional[int]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf Section.4
    
    >>> attack(2621, 8927)
    5
    >>> attack(6792605526025, 9449868410449)
    569
    >>> attack(30749686305802061816334591167284030734478031427751495527922388099381921172620569310945418007467306454160014597828390709770861577479329793948103408489494025272834473555854835044153374978554414416305012267643957838998648651100705446875979573675767605387333733876537528353237076626094553367977134079292593746416875606876735717905892280664538346000950343671655257046364067221469807138232820446015769882472160551840052921930357988334306659120253114790638496480092361951536576427295789429197483597859657977832368912534761100269065509351345050758943674651053419982561094432258103614830448382949765459939698951824447818497599, 109966163992903243770643456296093759130737510333736483352345488643432614201030629970207047930115652268531222079508230987041869779760776072105738457123387124961036111210544028669181361694095594938869077306417325203381820822917059651429857093388618818437282624857927551285811542685269229705594166370426152128895901914709902037365652575730201897361139518816164746228733410283595236405985958414491372301878718635708605256444921222945267625853091126691358833453283744166617463257821375566155675868452032401961727814314481343467702299949407935602389342183536222842556906657001984320973035314726867840698884052182976760066141)
    4221909016509078129201801236879446760697885220928506696150646938237440992746683409881141451831939190609743447676525325543963362353923989076199470515758399
    """
    f_ = rational_to_contfrac(e, n)
    for k, dg in convergents_from_contfrac(f_):
        edg = e * dg
        phi = edg // k

        x = n - phi + 1
        if x % 2 == 0 and is_perfect_square((x // 2) ** 2 - n):
            g = edg - phi * k
            return dg // g
    return None

N = 0x1fb7e02ec6ba11db84b1eeb3da2a09f1d1e4dd9ee969675dbf8c3f9a826d8f5f6e3a169a056a29346ef19bfcd4a8e3950e77d6873cc78b5fd07e24cae3e39e0008d148d674470d9cd5b2ec4ae72737705bc8c6ad94a98fb0597bd7a83dda37975ea59d30d00b14e79bfd5817e72b035124ef02101b94b47e0b9319e6e2c0b5fbf6a54570246f09c71240a862b898998cad0c3ab5989679bc3b9d7cb70d1952e685860b456812724c8d3868de684d9177832b8f0d9f0c093a7bc18a09e02bdc38d954a686c0a92675fd522a0f1958336628ea1d74d701b35bf8ee72c83ef0da7e57ee2f1d76922e9cfa0ce840ed3648028cf32fee08e527cbd25cf37d749007c09
e = 0x11ef05c01b36ff6fec8fd989e68a8d9c447252390178c0fe2810716e2ccfbb873f2b74ff9697e5318492b7d13acf6b7a7230ec94e45dea3db80aee6c421ca78ee0e37e3a760e62d2d9b16d4cc5fcfcf3dc9246ab282685b56722530ff772309b655438cb9349f7cad3535d9b2cac0bbc72d0eb9d1dbf86b7352fe341f6adc4dee95a8fb95d29558e6a8af9e33de04a9794d5b31af06f2557763fb5863876a707367d4658d4b654021c9baf12bff5dd8b7197a27542bc21657ddb3804fc061b343b1bc2bb8b47dd623bd0d3107f7dcf43888cc8ffc6722463f91bf23e6509d2084ec53c57101dce4c74e4821ae78b7aa36fb6bd72987d0812c23797441cb082095
print(attack(e,N))