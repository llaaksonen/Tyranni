"""
COMP.CS.100 Ohjelmointi 1
GUI-Projekti: Tyranni - juomapeli

------------------------***     PELIN SÄÄNNÖT        ***-----------------------
Peli itsessään on hyvin yksinkertainen, eikä siinä pärjääminen edellytä
aiempaa kokemusta pelin pelaamisesta. Miten peli toimii? Pelin alussa
sovitaan kollektiivisesti jokin sakkopanos, joka vaikuttaa pelin
haastavuusasteeseen; mitä pienempi sakkopanos, sitä tylsempi peli ja mitä
suurempi sakkopanos, sitä huonompi olo. Pelissä kukin pelaaja vuorollaan
nostaa korttipakasta kortin ja asettaa sen pöydälle. GUI-versiossa tämä
liikunnallinen rasite onkin korjattu vain yhdellä napin klikkauksella. Kun
kortti nostetaan pöydälle, pelaajat joutuvat reagoimaan nostetun kortin
numeeriseen arvoon (eli kortin maalla ei siis ole mitään väliä). Nämä
numeeriset arvot ovat pelissä tehtäviä yksilöllisiä, tai ryhmällisiä
suorituksia, joissa epäonnistuneita rangaistaan sakkopanoksen suuruisilla
rangaistushörpyillä. Koska kovimmiltakaan konkareilta ei edellytetä
täydellistä tehtävien ulkoamuistamista, graafinen käyttöliittymä kertoo
kunkin tehtävän tapauksessa, mitä nostettu kortti vastaa ja mitä
pelaajan/pelaajien tulee tehdä. Mainittakoot kuitenkin, että TÄRKEIMPINÄ
numeroina pidetään numeroita 4 ja 5, jossa kummankin tapauksessa kaikkien
pelaajien tulee mahdollisimman nopeasti huutaa "Tyranni!". Viimeiseksi
näin tehnyt joutuu juomaan. Muissa tehtävissä ei niinkään ole kyse
nopeudesta ja ne selviävätkin itse peliä pelaamalla ja käyttöliittymää
silmäilemällä. Ennalta-arvaamattomuus on keskeinen osa pelin kulkua.

------------------***     KÄYTTÖLIITTYMÄN OHJEISTUS        ***-----------------
Ohjelman käynnistäessä se kysyy pelaajilta ensiksi sakkopanoksen arvoa,
joka asetetaan käyttöliittymässä siihen toteutettua spinbox-elementtiä
hyödyntäen. Spinboxin arvot vaihtelevat välillä 1-10, sillä nämä ovat
realistisimmat arvot, joilla peliä voidaan pelata kunnolla (t. kokemus ja
empiiriset tutkimuset). Spinboxiin voidaan myös syöttää haluttu luku tuolta
määritetyltä väliltä. Sakkopanoksen arvo on oltava kokonaisluku (int). Kun
sakkopanos on syötetty, tulee painaa spinboxin alapuolella sijaitsevaa
OK-painiketta, jonka jälkeen peli voi alkaa. Seuraavan kortin saa aina
painamalla alimpana vasemmalla sijaitsevaa valkoista "Uusi
kortti"-painiketta, kunnes kortit loppuvat. Nostetun kortin arvoa vastaavan
tehtävän nimi ja sen ohje tulee aina tekstinä ruudulle, kortin kuvakkeen
alapuolelle. Pelin voi lopettaa sen aloitettuaan missä tahansa vaiheessa
painamalla punaista "Lopeta peli"-painiketta. Käyttöliittymän tarkoitus on
siis kertoa pelaajille, mitä heidän tulee tehdä käyttöliittymän ulkopuolella
oikeassa elämässä.
"""

import tkinter
from tkinter import *
from random import *


class Kayttoliittyma:
    """
    Tämä luokka edustaa pelin pelaamisen apuna käytettävää
    käyttöliittymää.
    """
    def __init__(self):
        """
        Rakentaja. Määrittää kaikki käyttöliittymässä tarvitut
        käyttöliittymäelementit ja muut olion muuttujat.
        """
        self.__paaikkuna = Tk()

        # Muokataan pääikkunaa
        self.__paaikkuna.title('Tyranni - juomapeli')
        self.__paaikkuna.configure(bg='green')
        self.__paaikkuna.iconphoto(False, tkinter.PhotoImage(
            file='pelikuvake.png'))
        self.__paaikkuna.geometry('800x800')

        self.__paaruutu = Frame(self.__paaikkuna, bg='green')
        self.__paaruutu.pack()

        self.__korttiruutu = Frame(self.__paaruutu, bg='green', width=275,
                                   height=399, pady=15)
        self.__korttiruutu.pack()

        self.__kanskortti = PhotoImage(file='kansikortti.png')

        # Määritetään kortin kuva, joka muuttuu pelin edetessä
        self.__kortinkuva = Label(self.__korttiruutu, image=self.__kanskortti)
        self.__kortinkuva.pack()

        self.__kortitjaljella_ruutu = Frame(self.__paaruutu, bg='green',
                                            width=200, height=20)
        self.__kortitjaljella_ruutu.pack()

        self.__tehtavan_ohjeruutu = Frame(self.__paaruutu, width=200,
                                          height=20, pady=15, bg='green')
        self.__tehtavan_ohjeruutu.pack()

        self.__tehtavan_tekstiruutu = Frame(self.__paaruutu, pady=5,
                                            bg='white')
        self.__tehtavan_tekstiruutu.pack()

        # Aloitusteksti
        self.__teksti = Label(self.__tehtavan_tekstiruutu, bg='white',
                              text="Tervetuloa pelaamaan Tyranni - "
                                   "juomapeliä! Valitse alta sopiva "
                                   "sakkopanos  ja aloita pelaaminen "
                                   "painamalla OK-painiketta",
                              font=('Arial', 12), wraplength=500)
        self.__teksti.pack()

        self.__spinbox = Spinbox(self.__tehtavan_tekstiruutu, from_=1,
                                 to=10, font=('Arial', 14))
        self.__spinbox.pack(pady=20)

        self.__okpainike = Button(self.__tehtavan_tekstiruutu, text="OK",
                                  width=10, height=1,
                                  command=self.tarkista_panos)
        self.__okpainike.pack()

        # Luodaan lista nostetuille korteille, jonne nostettujen korttien 
        # tiedostonimet sijoitetaan
        self.__nostetut_kortit = []

        # Määritetään muiden käyttöliittymäelementtien muuttujat. Nämä
        # saavat vasta pelin alustusvaiheessa None:sta poikkeavia arvoja
        self.__apukehyksenteksti = None
        self.__painikeruutu = None
        self.__uusikortti = None
        self.__sulkupainike = None
        self.__kortitloppu = None
        self.__panos = None
        self.__korttienmaara = None

        self.__paaikkuna.mainloop()

    def tarkista_panos(self):
        """
        Tarkistaa käyttäjän syöttämän panoksen. Jos panoksen arvo ei täytä
        vaatimuksia (eli jos se ei ole kokonaisluku väliltä 1-10), ohjelman
        ensisijaisessa tekstikentässä näytetään käyttäjälle virheilmoitus.
        """
        self.__panos = self.__spinbox.get()

        try:
            # Yritetään muuttaa sakkopanos kokonaisluvuksi
            self.__panos = int(self.__panos)

            if not 11 > self.__panos > 0:
                raise ValueError
            else:
                self.alusta_peli()

        except ValueError:
            self.__teksti.configure(text="Virheellinen syöte! Panoksen "
                                         "on oltava jokin nollaa "
                                         "suurempi kokonaisluku väliltä 1-10. "
                                         "Syötä panoksen"
                                         " arvo uudestan ja paina OK "
                                         "aloittaaksesi pelin.",
                                    font=('Arial', 12))

    def alusta_peli(self):
        """
        Alustaa pelin sellaiseen tilaan, jossa käyttäjän tarvitsee enää vain
        klikkailla painikkeita Tässä metodissa osa rakentajassa
        määritetyistä käyttöliittymäelementeistä saa None:sta poikkeavat arvot.
        """
        self.__spinbox.destroy()
        self.__okpainike.destroy()

        self.__tehtavan_tekstiruutu.configure(bg='green')
        self.__kortitjaljella_ruutu.configure(bg='green')

        self.__korttienmaara = Label(self.__kortitjaljella_ruutu,
                                     text="Kortteja jäljellä: 52",
                                     font=('Arial', 12))
        self.__korttienmaara.pack()

        self.__teksti.configure(text="Nosta kortti jatkaaksesi",
                                font=('Arial', 12), wraplengt=400,
                                width=50, height=8)

        # Luodaan ruutu uusille käyttöliittymässä tarvittaville painikkeille
        self.__painikeruutu = Frame(self.__paaruutu, bg='green', pady=15)
        self.__painikeruutu.pack()

        self.__uusikortti = Button(self.__painikeruutu, text="Nosta kortti",
                                   padx=35, pady=20,
                                   command=self.uusi_kortti, font=('Arial',
                                                                   12),
                                   width=10, height=1)
        self.__uusikortti.grid(row=0, column=0)
        self.__sulkupainike = Button(self.__painikeruutu, text="Lopeta peli",
                                     padx=35, pady=20,
                                     command=self.sulje_ohjelma, bg='red',
                                     font=('Arial', 12), width=10, height=1)
        self.__sulkupainike.grid(row=0, column=1)

        self.__apukehyksenteksti = Label(self.__tehtavan_ohjeruutu, text="",
                                         font='Arial, 20', bg='green')
        self.__apukehyksenteksti.pack()

    def sulje_ohjelma(self):
        """
        Sulkee ohjelman.
        """
        self.__paaikkuna.destroy()

    def uusi_kortti(self):
        """
        Luo satunnaisesti uuden kortin ja vaihtaa sen käyttöliittymään sille
        osoitettuun paikkaan. Satunnainen kortti luodaan satunnaisesta maan
        numeerisen arvon (1-risti, 2-ruutu, 3-hertta, 4-pata) ja
        satunnaisesta kortin numeerisen arvon muodostamasta tiedostonimestä
        (1-ässä, 13-kuningas, jne.). Jos silmukassa luotu kortti on jo
        käytetty, luodaaan uusi kunnes jokin käyttämätön kortti löytyy.
        """
        while True:
            # Otetaan satunnainen kortti "pakasta"
            kortin_maa = str(randint(1, 4))
            kortin_arvo = str(randint(1, 13))
            kortin_nimi = f"{kortin_arvo + kortin_maa}.png"

            if kortin_nimi not in self.__nostetut_kortit:
                self.__nostetut_kortit.append(kortin_nimi)

                # Päivitetään näytöllä näkyvä kortin kuva
                uusikortti = PhotoImage(file=kortin_nimi)
                self.__kortinkuva.configure(image=uusikortti)
                self.__kortinkuva.image = uusikortti
                break

        self.maarita_tehtava(int(kortin_arvo))

        # Tarkastetaan, onko kortteja enää jäljellä
        if len(self.__nostetut_kortit) == 52:
            self.__uusikortti.configure(command=self.loppuohjeet)
            self.kortteja_jaljella()

    def maarita_tehtava(self, tehtavan_numero):
        """
        Vaihtaa käyttöliittymässä teksteille tarkoitetut kohdat vastaamaan
        nostetun kortin nimeä ja sen tuomaa ohjeistusta. Jos nostetaan
        diktaattorikortti, nämä käyttöliittymäelementit saavat punaisen
        taustavärin. Muussa tapauksessa taustaväri on valkoinen.

        :param tehtavan_numero: int, nostetun kortin arvoa vastaava tehtävänro
        """
        # Pelissä esiintyvät tehtävät sanakirjassa niiden numeerista arvoa
        # vastaavilla paikoilla
        tehtavat = {
            1: "VESIPUTOUS! Kaikki pelaajat aloittavat juomaan omasta "
               "juomastaan, kun kortin nostanut pelaaja aloittaa juomaan. "
               "Kukin pelaaja saa laskea oman juomansa alansa vasta sitten, "
               "kun heitä edeltävä pelaaja on laskenut juomansa.",
            2: "ANNA 2! Kortin nostanut pelaaja määrää kenelle tahansa "
               "pelaajalle 2 hörppyä juotavaksi.",
            3: "OTA 3! Kortin nostanut pelaaja joutuu juomaan 3 hörppyä.",
            4: f'TYRANNI! Pelaajat joutuvat kaikki huutamaan: '
               f'"Tyranni". Viimeisin näin tehnyt pelaaja joutuu '
               f'juomaan {self.__panos} hörppyä.',
            5: f'TYRANNI! Pelaajat joutuvat kaikki huutamaan: '
               f'"Tyranni". Viimeisin näin tehnyt pelaaja joutuu '
               f'juomaan {self.__panos} hörppyä.',
            6: "123! Kortin nostanut pelaaja juo 1 hörpyn, häntä seuraava "
               "pelaaja juo 2 hörppyä ja niin edelleen.",
            7: f"KUKA TODENNÄKÖISIMMIN! Kortin nostanut pelaaja kysyy "
               f"kaikilta muilta pelaajilta, kuka kaikista pelaajista "
               f"todennäköisimmin tekisi asian X. Kun kaikki ovat "
               f"päättäneet, laskekaa kolmeen ja osoittakaa kukin "
               f"valitsemaanne pelaajaa samanaikaisesti. Eniten ääniä saanut "
               f"pelaaja juotuu juomaan {self.__panos} hörppyä.",
            8: f"SÄÄNTÖ! Kortin nostanut pelaaja saa päättää jonkin säännön, "
               f"jota on noudatettava koko pelin ajan. Sääntöä rikkova "
               f"joutuu aina juomaan {self.__panos} hörppyä. Sääntökortilla "
               f"voi myös kumota jonkin aiemmin langetetun säännön.",
            9: f"KATEGORIA! Kortin nostanut pelaaja saa päättää kategorian, "
               f"jonka aihepiiriin kukin pelaaja sanoo omalla vuorollaan "
               f"jonkin asian. Se kenellä ei lopuksi ole enää lisättävää, "
               f"joutuu juomaan {self.__panos} hörppyä.",
            10: f"TARINA! Kortin nostanut pelaaja aloittaa kertomaan "
                f"tarinaa, jota kukin pelaaja jatkaa omalla vuorollaan "
                f"lisäten yhden sanan muodostuneen tarinan loppuun. Se "
                f"pelaaja, joka ei muista/muistaa virheellisesti muodostetun "
                f"tarinan, joutuu juomaan {self.__panos} hörppyä.",
            11: f"KYSYMYSMESTARI! Kortin nostanut pelaaja saa missä "
                f"vaiheessa peliä kysyä keneltä tahansa pelaajalta jonkin "
                f"peliin liittymättömän kysymyksen. Kysymykseen vastannut "
                f"pelaaja joutuu juomaan {self.__panos} hörppyä.",
            12: f"VOSU! Kortin nostanut pelaaja saa valita kanssapelaajien "
                f"joukosta itselleen Vosun. Vosu joutuu aina juomaan saman "
                f"määrän hänen omistajansa juodessa. Vosuja saa olla pelissä "
                f"samanaikaisesti vain 1 kappale.",
            13: f"KUNINGASHÖRPPY! Kaikki muut pelaajat antavat kortin "
                f"nostaneelle pelaajalle 1 hörpyn omasta juomastaan."
        }

        tehtavan_teksti = tehtavat[tehtavan_numero]

        tehtavan_nimi = tehtavan_teksti.split("!")[0]
        tehtavan_ohje = tehtavan_teksti.split("!")[1]

        if tehtavan_numero == 4 or tehtavan_numero == 5:
            self.__teksti.configure(text=tehtavan_ohje, bg='red')
            self.__apukehyksenteksti.configure(text=tehtavan_nimi, bg='red')
        else:
            self.__teksti.configure(text=tehtavan_ohje, bg='white')
            self.__apukehyksenteksti.configure(text=tehtavan_nimi, bg='green')

        self.kortteja_jaljella()

    def kortteja_jaljella(self):
        """
        Laskee jäljellä olevien korttien määrän ja vaihtaa sen
        käyttöliittymään sille osoitettuun kohtaan joka kierroksen alussa.
        """
        maara = 52 - len(self.__nostetut_kortit)
        self.__korttienmaara.configure(text=f"Kortteja jäljellä: {maara}",
                                       font=('Arial', 12), bg='white')

    def loppuohjeet(self):
        """
        Vaihtaa korttikuvakkeen takaisin kansikorttiin, ilmoittaa
        käyttäjälle korttien loppumisesta ja antaa käyttäjälle tarvittavat
        loppuohjeet käyttöliittymässä.
        """
        self.__kortinkuva.configure(image=self.__kanskortti)

        self.__apukehyksenteksti.configure(bg='green')
        self.__apukehyksenteksti.configure(text="KORTIT LOPPU!")

        self.__teksti.configure(bg='white')
        self.__teksti.configure(text="Kortit ovat loppuneet ja peli on "
                                     "tullut päätökseensä. Käykää juomassa "
                                     "vettä ja kokeilkaa peliä jonkin ajan "
                                     "päästä uudestaan!")


def main():
    Kayttoliittyma()


if __name__ == '__main__':
    main()
