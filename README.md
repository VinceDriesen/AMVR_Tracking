
# **Verslag**

## **Techniek 1: Marker-based AR (met ArUco)**

[1] S. Garrido-Jurado, R. Muñoz-Salinas, F. J. Madrid-Cuevas, and M. J. Marín-Jiménez, “Automatic generation and detection of highly reliable fiducial markers under occlusion,” *Pattern Recognition*, vol. 47, no. 6, pp. 2280–2292, Jun. 2014, doi: 10.1016/j.patcog.2014.01.005.

[2] R. Xavier, A. A. G. Nascimento, and P. R. P. Filho, “Accuracy analysis of augmented reality markers for visual mapping and localization,” in *Proc. Int. Conf. on Graphics and Interaction (SIBGRAPI)*, 2019, pp. 152–159, doi: 10.1109/SIBGRAPI.2019.00029.

[3] S. Poroykov, E. Radykova, and A. Mozgovoy, “Modeling ArUco markers images for accuracy analysis of their 3D pose estimation,” in *Proc. GraphiCon*, 2020, pp. 97–102. [Online]. Available: [https://ceur-ws.org/Vol-2744/short14.pdf](https://ceur-ws.org/Vol-2744/short14.pdf)

[4] R. Sablatnig, C. Schmid, and M. Wimmer, “Improving marker-based tracking for augmented reality in underwater environments,” in *Proc. Eurographics Workshop on Graphics and Cultural Heritage*, 2018, pp. 21–30, doi: 10.2312/gch.20181337.

[5] I. Ormesher, “Augmented reality using fiducial markers,” *Medium*, Aug. 2019. [Online]. Available: [https://medium.com/data-science/augmented-reality-using-fiducial-markers-b8124b8f528](https://medium.com/data-science/augmented-reality-using-fiducial-markers-b8124b8f528)

---

### **Hoe werkt het?**

Deze techniek gebruikt een camera om te zoeken naar specifieke, vooraf gedefinieerde vierkante markers.
Elke marker heeft een uniek patroon dat overeenkomt met een **ID** uit een *dictionary*. Dit is bij ons `DICT_4X4_50`, maar is niet altijd zo. In de toturial zelf werd een andere gebruikt.
Wanneer de software een marker vindt, identificeert het de vier hoekpunten.

Met deze vier punten in de 2D-camera-afbeelding, en de bekende 3D-vorm van de marker, kan het een wiskundige berekeningen uitvoeren om zo de exacte **3D-positie en rotatie van de camera** ten opzichte van de marker te vinden.
Zodra deze positie bekend is, kan een virtueel object (zoals een video bij ons) met de juiste **perspectiefvervorming** op de marker worden getekend.

---

### **Voordelen**

* **Snel en efficiënt:** ArUco-detectie is licht voor de processor en kan in real-time draaien op bijna elk apparaat [1].
* **Robuust:** Werkt goed bij slechte belichting, gedeeltelijke bedekking (soms), of snelle bewegingen, vooral als caching wordt toegepast wat bij ons het geval is indien dit aan wordt gezet [4].
* **Hoge precisie:** Omdat de marker exact bekend is, is de positiebepaling extreem nauwkeurig [2], [3].
* **Eenvoudige context:** De marker-ID geeft direct context (bijv. marker #23 = “motorblok”), zodat de juiste AR-informatie getoond kan worden [5].

---

### **Nadelen**

* **Visueel storend:** Er moet altijd een fysieke, vaak lelijke zwart-witte marker in beeld zijn, wat de realistische illusie vermindert [4].
* **Beperkt gebied:** De AR werkt alleen zolang de camera de marker ziet; zodra de marker uit beeld is, verdwijnt het AR-object [1].

---

### **Voorbeeldapplicatie: Industrieel onderhoud & robotica**

**Waarom beste keuze:**
In een fabriek of bij een complexe machine zijn **precisie en snelheid** belangrijker dan visuele esthetiek.

**Hoe gebruikt:**

Een monteur richt een tablet op een machine die is voorzien van kleine ArUco-tags.
Wanneer de camera bijvoorbeeld tag #17 (bv het oliefilter) ziet, toont de app pijlen die precies aangeven hoe het filter moet worden losgeschroefd.
Een robotarm in een fabriekshal kan via een marker op de grijper zijn positie tot op de millimeter nauwkeurig kalibreren [2], [3].

---

## **Techniek 2: Markerless AR (Feature-based / SLAM)**

[6] A. Kamat, P. Bhargava, and S. Kamat, “A survey of marker-less tracking and registration techniques for augmented reality,” *Sensors*, vol. 19, no. 15, pp. 1–28, Jul. 2019, doi: 10.3390/s19153439.

[7] K. S. Chaudhari and S. Borkar, “A survey on marker-less augmented reality,” *Int. J. Eng. Trends Technol. (IJETT)*, vol. 10, no. 13, pp. 655–658, Apr. 2014, doi: 10.14445/22315381/IJETT-V10P328.

[8] H. B. Kumar and P. Gupta, “Monocular visual SLAM for markerless tracking algorithm to augmented reality,” *Intell. Autom. Soft Comput.*, vol. 35, no. 2, pp. 1367–1380, Feb. 2022, doi: 10.32604/iasc.2022.027466.

[9] A. P. Brito, A. M. R. da Costa, and C. A. Ferreira, “In-depth review of augmented reality: Tracking technologies,” *Sensors*, vol. 23, no. 2, p. 743, Jan. 2023, doi: 10.3390/s23020743.

[10] T. Scargill, “Context-aware markerless augmented reality for shared educational spaces,” in *Proc. IEEE Int. Symp. on Mixed and Augmented Reality (ISMAR) Doctoral Consortium*, Bari, Italy, 2021, pp. 1–4. [Online]. Available: [https://sites.duke.edu/timscargill/files/2021/10/ISMAR21_Doctoral_Consortium_CameraFinal.pdf](https://sites.duke.edu/timscargill/files/2021/10/ISMAR21_Doctoral_Consortium_CameraFinal.pdf)

---

### **Hoe werkt het?**

Deze techniek maakt gebruik van **feature-detectiealgoritmes** om een referentieafbeelding te matchen binnen een live omgeving [6], [7].
**Features** zijn hierbij typisch hoeken, texturen of patronen in de referentieafbeelding.
Deze feature-detectie wordt ook toegepast op de live video-feed, en met behulp van een feature-matching-algoritme worden de features van de referentieafbeelding zo goed mogelijk gematcht met de features die in de video worden gedetecteerd [8].

Het wordt bijvoorbeeld gebruikt bij **SLAM (Simultaneous Localization and Mapping)**, waarbij features worden gedetecteerd, opgeslagen en opnieuw herkend om zo een 3D-kaart van deze features op te bouwen, waarin de video-feed zich kan positioneren [8], [9].
Moderne versies, zoals **ARKit** of **ARCore**, voegen ook **vlakdetectie (plane detection)** toe, waarbij horizontale en verticale oppervlakken worden herkend [9].

---

### **Voordelen**

* **Realistisch en immersief:** AR-objecten lijken ‘echt’ in de wereld te staan, zonder markers [6].
* **Werkt overal:** Geen speciale marker nodig; een omgeving met voldoende textuur is genoeg [7].
* **Persistentie:** Objecten blijven op hun plek, zelfs als je even wegkijkt [8].

---

### **Nadelen**

* **Zwaar en complex:** Vereist meer rekenkracht (CPU/GPU) dan marker-detectie [8].
* **Minder stabiel:** Kan last hebben van ‘drifting’ of ‘jittering’ [6], [9].
* **Omgevingsafhankelijk:** Werkt slecht op gladde of monotone oppervlakken [7].
* **Opstarttijd:** Moet eerst de omgeving “scannen” voordat objecten stabiel geplaatst kunnen worden [9].

---

### **Voorbeeldapplicatie: Meubel-apps & AR-games**

**Waarom beste keuze:**
Voor consumentenapps is **realistisch uiterlijk en gebruiksgemak** belangrijker dan absolute precisie [6], [7].

**Hoe gebruikt:**

Bijvoorbeeld in de **IKEA Place** app. De gebruiker scant de woonkamer door de telefoon te bewegen; de app detecteert de vloer.
Vervolgens kiest de gebruiker een virtuele zetel uit de catalogus en plaatst deze op de vloer.
De gebruiker kan vervolgens rondlopen om te zien of het meubelstuk goed in het interieur past [9], [10].


