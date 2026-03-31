# Všechny endpointy

- všechny endpointy vrací HTTP STATUS CODE 200, pokud nenastane chyba

## [GET] /

### GET /

- vrací jakýkoliv text, který obsahuje `Hello from Flask!`

## [GET, POST] /messages

### GET /messages

- vrací všechny zprávy přihlášenému uživateli

- nepřihlášenému 403 (forbiden)

### POST /messages

- přijme zprávu a vrací 201 (created) při správném zapsání do databáze

- při chybě zpracování zprávy vrací 500 (internal server error)

## [GET, PUT, DELETE] /message/&lt;uuid&gt;

### GET /message/&lt;uuid&gt;

- vrací vybranou zprávu se všemi informacemi

- 404 (not found) při neexistující zprávě

### PUT /message/&lt;uuid&gt;

- upraví zprávu podle nových dat v přijmutém dotazu a vrací 204 (no content)

### DELETE /message/&lt;uuid&gt;

- smaže dannou zprávu a vrací 204 (no content)
