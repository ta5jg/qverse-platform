# Q-Verse Forge Admin UI

This is the web admin interface for Q-Verse Forge.

## Local development

```bash
cd frontend/admin
npm install
npm run dev
```

## Production build

```bash
cd frontend/admin
npm install
npm run build
```

Deploy the generated `dist` directory behind Nginx, for example under:

```text
https://api.q-verse.io/admin/forge/
```

The frontend talks to:

```text
https://api.q-verse.io/forge
```
