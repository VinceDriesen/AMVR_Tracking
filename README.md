
# **Verslag**

## **Techniek 1: Marker-based AR (met ArUco)**

[1] S. Garrido-Jurado, R. Muñoz-Salinas, F. J. Madrid-Cuevas, and M. J. Marín-Jiménez, “Automatic generation and detection of highly reliable fiducial markers under occlusion,” Pattern Recognition, vol. 47, no. 6, pp. 2280–2292, Jun. 2014, doi: https://doi.org/10.1016/j.patcog.2014.01.005.
‌

[2] R. S. Xavier, Bruno, and Luiz, “Accuracy Analysis of Augmented Reality Markers for Visual Mapping and Localization,” Oct. 2017, doi: https://doi.org/10.1109/wvc.2017.00020.


[3] A. Poroykov, P. Kalugin, S. Shitov, and I. Lapitskaya, “Modeling ArUco Markers Images for Accuracy Analysis of Their 3D Pose Estimation,” Proceedings of the 30th International Conference on Computer Graphics and Machine Vision (GraphiCon 2020). Part 2, pp. short14-1short14-7, Dec. 2020, doi: https://doi.org/10.51130/graphicon-2020-2-4-14.
‌

[4] J. Cejka, Marek Zuzi, Panagiotis Agrafiotis, Dimitrios Skarlatos, F. Bruno, and Fotis Liarokapis, “Improving Marker-Based Tracking for Augmented Reality in Underwater Environments.,” pp. 21–30, Jan. 2018, doi: https://doi.org/10.2312/gch.20181337.

---

### **Hoe werkt het?** [3]

Deze techniek gebruikt een camera om te zoeken naar specifieke, vooraf gedefinieerde vierkante markers.
Elke marker heeft een uniek patroon dat overeenkomt met een **ID** uit een *dictionary*. Dit is bij ons `DICT_4X4_50`, maar is niet altijd zo. In de toturial zelf werd een andere gebruikt.
Wanneer de software een marker vindt, identificeert het de vier hoekpunten.

Met deze vier punten in de 2D-camera-afbeelding, en de bekende 3D-vorm van de marker, kan het een wiskundige berekeningen uitvoeren om zo de exacte **3D-positie en rotatie van de camera** ten opzichte van de marker te vinden.
Zodra deze positie bekend is, kan een virtueel object (zoals een video bij ons) met de juiste **perspectiefvervorming** op de marker worden getekend.

---

### **Voordelen**

* **Snel en efficiënt:** ArUco-detectie is licht voor de processor en kan in real-time draaien op bijna elk apparaat [2].
* **Robuust:** Werkt goed bij slechte belichting, gedeeltelijke bedekking (soms), of snelle bewegingen, vooral als caching wordt toegepast wat bij ons het geval is indien dit aan wordt gezet [2], [4].
* **Hoge precisie:** Omdat de marker exact bekend is, is de positiebepaling extreem nauwkeurig [1].
* **Eenvoudige context:** De marker-ID geeft direct context (bijv. marker #23 = “motorblok”), zodat de juiste AR-informatie getoond kan worden [3].

---

### **Nadelen**

* **Visueel storend:** Er moet altijd een fysieke, vaak lelijke zwart-witte marker in beeld zijn, wat de realistische illusie vermindert. [3]
* **Beperkt gebied:** De AR werkt alleen zolang de camera de marker ziet; zodra de marker uit beeld is, verdwijnt het AR-object [1].

---

### **Voorbeeldapplicatie: Industrieel onderhoud & robotica** [1]

**Waarom beste keuze:**
In een fabriek of bij een complexe machine zijn **precisie en snelheid** belangrijker dan visuele esthetiek.

**Hoe gebruikt:**

Een monteur richt een tablet op een machine die is voorzien van kleine ArUco-tags.
Wanneer de camera bijvoorbeeld tag #17 (bv het oliefilter) ziet, toont de app pijlen die precies aangeven hoe het filter moet worden losgeschroefd.
Een robotarm in een fabriekshal kan via een marker op de grijper zijn positie tot op de millimeter nauwkeurig kalibreren.

---

## **Techniek 2: Markerless AR (Feature-based / SLAM)**

[6] A. Kamat, P. Bhargava, and S. Kamat, “A survey of marker-less tracking and registration techniques for augmented reality,” *Sensors*, vol. 19, no. 15, pp. 1–28, Jul. 2019, doi: 10.3390/s19153439.

[7] H. B. Kumar and P. Gupta, “Monocular visual SLAM for markerless tracking algorithm to augmented reality,” *Intell. Autom. Soft Comput.*, vol. 35, no. 2, pp. 1367–1380, Feb. 2022, doi: 10.32604/iasc.2022.027466.

[8] A. P. Brito, A. M. R. da Costa, and C. A. Ferreira, “In-depth review of augmented reality: Tracking technologies,” *Sensors*, vol. 23, no. 2, p. 743, Jan. 2023, doi: 10.3390/s23020743.

---

### **Hoe werkt het?**

Deze techniek maakt gebruik van **feature-detectiealgoritmes** om een referentieafbeelding te matchen binnen een live omgeving [6].
**Features** zijn hierbij typisch hoeken, texturen of patronen in de referentieafbeelding.
Deze feature-detectie wordt ook toegepast op de live video-feed, en met behulp van een feature-matching-algoritme worden de features van de referentieafbeelding zo goed mogelijk gematcht met de features die in de video worden gedetecteerd [7].

Het wordt bijvoorbeeld gebruikt bij **SLAM (Simultaneous Localization and Mapping)**, waarbij features worden gedetecteerd, opgeslagen en opnieuw herkend om zo een 3D-kaart van deze features op te bouwen, waarin de video-feed zich kan positioneren [7], [8].
Moderne versies, zoals **ARKit** of **ARCore**, voegen ook **vlakdetectie (plane detection)** toe, waarbij horizontale en verticale oppervlakken worden herkend [8].

---

### **Voordelen**

* **Realistisch en immersief:** AR-objecten lijken ‘echt’ in de wereld te staan, zonder markers [6].
* **Werkt overal:** Geen speciale marker nodig; een omgeving met voldoende textuur is genoeg.
* **Persistentie:** Objecten blijven op hun plek, zelfs als je even wegkijkt [7].

---

### **Nadelen**

* **Zwaar en complex:** Vereist meer rekenkracht (CPU/GPU) dan marker-detectie [7].
* **Minder stabiel:** Kan last hebben van ‘drifting’ of ‘jittering’ [6], [8].
* **Omgevingsafhankelijk:** Werkt slecht op gladde of monotone oppervlakken.
* **Opstarttijd:** Moet eerst de omgeving “scannen” voordat objecten stabiel geplaatst kunnen worden [8].

---

### **Voorbeeldapplicatie: Meubel-apps & AR-games**

**Waarom beste keuze:**
Voor consumentenapps is **realistisch uiterlijk en gebruiksgemak** belangrijker dan absolute precisie [6].

**Hoe gebruikt:**

Bijvoorbeeld in de **IKEA Place** app. De gebruiker scant de woonkamer door de telefoon te bewegen; de app detecteert de vloer.
Vervolgens kiest de gebruiker een virtuele zetel uit de catalogus en plaatst deze op de vloer.
De gebruiker kan vervolgens rondlopen om te zien of het meubelstuk goed in het interieur past [8].


