# AnkiConnect Agent Guide

- **Documentation**: https://git.sr.ht/~foosoft/anki-connect

AnkiConnect plugin exposes Anki via HTTP API at `http://localhost:8765`.

## Request Format

```json
{"action": "actionName", "version": 6, "params": {...}}
```

## Response Format

```json
{"result": ..., "error": ...}
```

## Main Actions

| Category | Actions |
|----------|---------|
| Decks | `deckNames`, `createDeck`, `getDeckStats`, `changeDeck`, `deleteDecks` |
| Notes | `addNote`, `addNotes`, `findNotes`, `notesInfo`, `updateNote`, `deleteNotes` |
| Cards | `findCards`, `cardsInfo`, `suspend`, `unsuspend`, `areDue` |
| Models | `modelNames`, `modelFieldNames`, `createModel`, `updateModelTemplates` |
| Media | `storeMediaFile`, `retrieveMediaFile`, `getMediaDirPath` |
| GUI | `guiBrowse`, `guiAddCards`, `guiCurrentCard` |
| Stats | `getDeckStats`, `getNumCardsReviewedToday`, `cardReviews` |
| Misc | `multi` (batch), `sync`, `requestPermission`, `version` |

## Examples

```bash
# Using wrapper (scripts/anki.py)
python3 scripts/anki.py deckNames
python3 scripts/anki.py findCards --params '{"query": "deck:Korean::TOPIK1"}'

# Raw curl
curl -s localhost:8765 -X POST -d '{"action": "deckNames", "version": 6}'
```

## Scripting

Wrapper `scripts/anki.py` simplifies calls and outputs `.result` directly:

```bash
python3 scripts/anki.py [action] --params '{...}' [--url http://localhost:8765]
```

**Chaining calls**: Use xargs to pipe output into next call.

```bash
python3 scripts/anki.py findCards --params '{"query": "deck:MyDeck"}' \
  | xargs -I {} python3 scripts/anki.py cardsInfo --params '{"cards": {}}' \
  | jq '...'
```

**Raw curl** (when wrapper unavailable):

```bash
# xargs pattern
curl -s localhost:8765 -X POST -d '{"action": "findCards", "version": 6, "params": {"query": "deck:MyDeck"}}' \
  | jq -c '.result' \
  | xargs -I {} curl -s localhost:8765 -X POST -d '{"action": "cardsInfo", "version": 6, "params": {"cards": {}}}' \
  | jq '.result'
```

Notes:
- Wrapper outputs `.result` directly; raw curl needs `jq '.result'`
- Use `jq -c` (compact) to keep JSON on one line for xargs
