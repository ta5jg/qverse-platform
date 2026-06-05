export const apiClient={get:async(url)=>fetch(url).then(r=>r.json())};
