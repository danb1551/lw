# Všechny endpointy

- všechny endpointy vrací HTTP STATUS CODE 200, pokud nenastane chyba

## [GET] /

### GET /

- vrací jakýkoliv text, který obsahuje `Hello from Flask!`

## [GET, POST] /messages

### GET /messages

- vrací všechny zprávy přihlášenému uživateli

- nepřihlášenému 403

### POST /messages

- přijme zprávu a vrací 201 při správném zaosání do databáze

- při chybě zpracování zprávy vrací 500

## [GET, PUT, DELETE] /message/<uuid>

### GET /message/<uuid>

- vrací vybranou zprávu se všemi informacemi

- 404 při neexistující zprávě

### PUT /message/<uuid>

- upraví zprávu podle nových dat v přijmutém dotazu

### DELETE /message/<uuid>

- smaže dannou zprávu a vrací 204
