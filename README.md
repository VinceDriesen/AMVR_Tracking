# Verslag

## Techniek 1: Marker-based AR (met ArUco)

### Hoe werkt het?
Deze techniek gebruikt een camera om te zoeken naar specifieke, vooraf gedefinieerde vierkante markers (in ons geval **ArUco-markers**).

Elke marker heeft een uniek patroon dat overeenkomt met een **ID** uit een *dictionary* (bijvoorbeeld `DICT_4X4_50`).

Wanneer de software (OpenCV) een marker vindt, identificeert het de vier hoekpunten.

Met deze vier punten in de 2D-camera-afbeelding, en de bekende 3D-vorm van de marker (een plat vierkant), kan het een wiskundige berekening uitvoeren (`cv2.findHomography`).

Deze berekening geeft de exacte **3D-positie en rotatie van de camera** ten opzichte van de marker.

Zodra deze positie bekend is, kan een virtueel object (zoals een video of 3D-model) met de juiste **perspectiefvervorming** op de marker worden getekend.

### Voordelen
- **Snel en efficiënt:** ArUco-detectie is licht voor de processor en kan in real-time draaien op bijna elk apparaat.  
- **Robuust:** Werkt goed bij slechte belichting, gedeeltelijke bedekking (soms), of snelle bewegingen. Indien caching wordt toegepast.
- **Hoge precisie:** Omdat de marker exact bekend is, is de positiebepaling extreem nauwkeurig.  
- **Eenvoudige context:** De marker-ID geeft direct context (bijv. marker #23 = “motorblok”), zodat de juiste AR-informatie getoond kan worden.  

### Nadelen
- **Visueel storend:** Je moet altijd een fysieke, vaak lelijke, zwart-witte marker in beeld hebben, wat de realistische illusie vermindert.  
- **Beperkt gebied:** De AR werkt alleen zolang de camera de marker ziet. Zodra de marker uit beeld is, verdwijnt het AR-object.  

### Voorbeeldapplicatie: Industrieel onderhoud & robotica
**Waarom beste keuze:**  
In een fabriek of bij een complexe machine zijn **precisie en snelheid** belangrijker dan visuele esthetiek. 

**Hoe gebruikt:**  
Een monteur richt een tablet op een machine die is voorzien van kleine ArUco-tags. Wanneer de camera bijvoorbeeld tag #17 (het oliefilter) ziet, toont de app pijlen die precies aangeven hoe het filter moet worden losgeschroefd.  
Een robotarm in een fabriekshal kan via een marker op de grijper zijn positie tot op de millimeter nauwkeurig kalibreren.

---

## Techniek 2: Markerless AR (Feature-based / SLAM)

### Hoe werkt het?
Deze techniek zoekt niet naar één specifieke marker, maar naar honderden kleine, unieke **features** in de omgeving (bijv. hoeken, texturen, of patronen).

Het gebruikt algoritmes zoals **SLAM (Simultaneous Localization and Mapping)** om een 3D-kaart van deze features op te bouwen.

Terwijl de camera beweegt, vergelijkt het constant de nieuwe features die het ziet met de bestaande 3D-kaart, zodat het zijn **positie en oriëntatie** in de ruimte kan bepalen.

Moderne versies (zoals **ARKit** of **ARCore**) voegen ook **vlakdetectie (plane detection)** toe, waarbij ze horizontale (vloeren, tafels) en verticale (muren) oppervlakken herkennen.

### Voordelen
- **Realistisch en immersief:** AR-objecten lijken ‘echt’ in de wereld te staan, zonder markers. Je kunt er omheen lopen.  
- **Werkt overal:** Geen speciale marker nodig; een omgeving met voldoende textuur (zoals een woonkamer) is genoeg.  
- **Persistentie:** Objecten blijven op hun plek, zelfs als je even wegkijkt en terugkomt.  

### Nadelen
- **Zwaar en complex:** Vereist veel meer rekenkracht (CPU/GPU) dan marker-detectie.  
- **Minder stabiel:** Kan last hebben van ‘drifting’ (object verschuift langzaam) of ‘jittering’ (trillen).  
- **Omgevingsafhankelijk:** Werkt slecht op gladde of monotone oppervlakken (zoals witte muren of glimmende vloeren).  
- **Opstarttijd:** Moet eerst de omgeving “scannen” voordat objecten stabiel geplaatst kunnen worden.  

### Voorbeeldapplicatie: Meubel-apps & AR-games
**Waarom beste keuze:**  
Voor consumentenapps is **realistisch uiterlijk en gebruiksgemak** belangrijker dan absolute precisie.  

**Hoe gebruikt:**  
Bijvoorbeeld in de **IKEA Place** app. De gebruiker scant de woonkamer door de telefoon te bewegen; de app detecteert de vloer. Vervolgens kiest de gebruiker een virtuele zetel uit de catalogus en plaatst deze op de vloer.  
De gebruiker kan vervolgens rondlopen om te zien of het meubelstuk goed in het interieur past.
