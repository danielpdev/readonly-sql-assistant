# Pregătire pentru interviu — Read-only SQL Assistant

Roluri țintă: Applied AI / Data Backend.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: An LLM may propose SQL, but a separate SQLite read-only URI, query-only connection and authorizer decide whether it can run. Table/function allowlists, operation limits and row caps constrain execution.

## Cinci întrebări

1. De ce promptul read-only nu este suficient?
2. Ce blochează authorizer-ul?
3. Cum limitezi query cost?
4. Cum explici truncation?
5. Cum protejezi datele per tenant?

## Exercițiu înainte de a aplica

Add a reviewed semantic layer, tenant row filtering and more labeled question/SQL pairs.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
