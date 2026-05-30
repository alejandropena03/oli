# Playbooks de Oli

Workflows reutilizables derivados de misiones repetidas.

Los playbooks se proponen automáticamente cuando Oli detecta repetición con estructura similar. El usuario aprueba o rechaza.

## Estado actual

Sin playbooks aprobados. Primer candidato identificado en Slice-001 (research-brief-v1).

## Formato

Ver `tdd/schemas/playbook.ts` cuando esté disponible.

```
nombre: research-brief-v1
trigger: "investiga [tema] y dame un brief"
pasos: [identificar_sujetos, research_por_sujeto, sintetizar, validar, entregar]
variables: [tema, sujetos, formato_output]
tiempo_estimado: 8 min
costo_estimado: $0.12
mision_origen: slice-001
```
