# Evoluční algoritmy pro konstrukci 2D mostů ve hře Poly Bridge

##  Úvod 

Poly Bridge je logická simulační hra zaměřená na návrh mostů. Hráči využívají různé materiály k tvorbě 2D konstrukcí, které musí odolávat zátěži projíždějících vozidel, které se snaží dostat přes řeku a zároveň splňovat rozpočtová omezení. Hra se opírá o realistické fyzikální principy a poskytuje prostor pro experimentování s různými stavebními technikami. Cílem práce je navrhnout evoluční algoritmus, který bude pro vybrané úrovně navrhovat stabilní a levné mosty.

## Řešení

### Fyzikální prostředí

Nejprve bylo nutné navrhnout fyzikální prostředí, které by věrně simulovalo podmínky ve hře Poly Bridge. K tomuto účelu jsme použili programovací jazyk Python ve spojení s fyzikálním enginem Box2D. Poté jsme zvolili sadu testů, které ověřily, že naše simulace skutečně odpovídá prostředí ve hře.

### Evolučňí algoritmy

Bylo navrženo několik typů kódování jedince několik a genetických operátorů. Nejúspěšnější z nich reprezentovali jedince jako graf s rovinným nakreslením. Fitness jedince primárně tvořila vzdálenost od bodu na druhé straně řeky, sekundárně pak cena mostu.

## Řešení navrhnutá člověkem vs Řešení navrhnutá evolucí

obrázky

## Výsledky

Navržený algoritmus zvládnul vyřešit první tři se čtyř zvolených úrovní. Některá řešení nelezená evolucí byla levnější, než řešení navrhnutá člověkem. 

## Poděkování

Chtěl bych poděkovat mému vedoucímu Mgr. Romanovi Nerudovi CSc. za jeho cenné rady a připomínky.
