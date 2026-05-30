# ADR-018 — Multi-user y trabajo en equipo

**Estado:** accepted
**Fecha:** 2026-05-26
**Decisión del founder:** Oli soporta equipos desde V1. El trabajo en equipo con IA es un gap real del mercado.

---

## Contexto

La mayoría de agentes de IA son estrictamente personales: un usuario, una instancia, una memoria.
Oli puede ser diferente — y esa diferencia es una ventaja competitiva real.

El founder lo identificó correctamente: pocos saben cómo compartir contexto de IA en equipo,
cómo coordinar misiones entre miembros, cómo mantener la memoria de empresa compartida
mientras se respeta la privacidad individual.

---

## Los 3 tipos de memoria en un equipo

```
MEMORIA PERSONAL (privada — solo el miembro la ve)
  → Preferencias individuales
  → Historial personal de misiones
  → Correcciones propias
  → Notas privadas

MEMORIA DE EQUIPO / EMPRESA (compartida — todos la ven)
  → ICP, producto, roadmap, decisiones
  → Playbooks aprobados
  → Contexto de clientes y proyectos
  → Estándares de trabajo del equipo

MEMORIA DE MISIÓN (compartida con el equipo relevante)
  → Misiones asignadas a múltiples miembros
  → Evidencia compartida
  → Reportes visibles para el equipo
```

---

## Roles en el equipo

```python
class TeamRole(Enum):
    OWNER      = "owner"     # El founder. Control total. Puede todo.
    ADMIN      = "admin"     # Puede crear misiones, gestionar miembros, ver todo
    OPERATOR   = "operator"  # Puede crear y ejecutar misiones dentro de su scope
    VIEWER     = "viewer"    # Solo puede ver misiones y resultados asignados
```

---

## Modelo de permisos con equipo

El sistema de clases (0-4) se mantiene igual, pero se agrega una capa de **scope de equipo**:

```python
class MissionScope(Enum):
    PERSONAL    = "personal"   # Solo el creador ve y controla
    TEAM        = "team"       # Todo el equipo ve el progreso
    ASSIGNED    = "assigned"   # Asignada a un miembro específico

class PermissionPolicy:
    # Quién puede aprobar qué según el rol
    approval_matrix = {
        PermissionClass.CLASS_3: [Role.OWNER, Role.ADMIN],  # comunicación externa
        PermissionClass.CLASS_4: [Role.OWNER],               # destructivo — solo owner
        PermissionClass.CLASS_2: [Role.OWNER, Role.ADMIN, Role.OPERATOR],
        PermissionClass.CLASS_1: [Role.OWNER, Role.ADMIN, Role.OPERATOR],
        PermissionClass.CLASS_0: "auto",  # cualquier rol
    }
```

---

## Cómo funciona la memoria compartida

```
ESCRITURA:
  MemoryCuratorSuboperator sugiere → 
  Si es memoria personal → se guarda directo (ADR-009: auto-write)
  Si es memoria de empresa → pasa por el OWNER o ADMIN para aprobación
  (el equipo no puede contaminar la memoria de empresa sin aprobación)

LECTURA (RAG):
  Cada miembro recupera:
    ✓ Su memoria personal completa
    ✓ La memoria de empresa completa
    ✗ La memoria personal de otros miembros (nunca)
    ✓ La memoria de misiones asignadas a él o compartidas con su equipo
```

---

## Las misiones en equipo

### Asignación

```python
mission = Mission(
    created_by="alejandro",
    assigned_to="carlos",      # otro miembro del equipo
    scope=MissionScope.ASSIGNED,
    # Carlos recibe notificación, puede ejecutar la misión
    # Alejandro puede ver el progreso y el resultado
)
```

### Misiones colaborativas

Dos miembros trabajando en la misma misión con sub-tareas:

```python
mission = Mission(
    created_by="alejandro",
    scope=MissionScope.TEAM,
    plan=MissionPlan(steps=[
        MissionStep(assigned_to="carlos",    executor="TechnicalArchitect"),
        MissionStep(assigned_to="alejandro", executor="MarketResearch"),
        MissionStep(assigned_to=None,        executor="Orchestrator"),  # Oli sintetiza
    ])
)
```

### Aprobaciones en equipo

Cuando una misión necesita aprobación clase 3+:
- Si el creador está disponible → le llega a él
- Si no está disponible → escala al siguiente con permisos (ADMIN)
- Nunca bloquea una misión esperando indefinidamente

---

## Playbooks de equipo

Los playbooks tienen visibilidad:

```python
class PlaybookVisibility(Enum):
    PERSONAL = "personal"  # solo el creador puede usarlo
    TEAM     = "team"      # todo el equipo puede ejecutarlo
    TEMPLATE = "template"  # plantilla base — cualquiera puede hacer fork
```

Un playbook de equipo permite que cualquier miembro ejecute la misma automatización
con el mismo nivel de calidad — sin que cada uno tenga que redescubrir cómo hacerlo.

---

## Onboarding de un nuevo miembro

```
1. OWNER invita a nuevo miembro con rol asignado
2. Oli hace onboarding guiado:
   "Hola [nombre]. Soy Oli. Voy a contarte cómo trabajamos acá."
3. Oli comparte el contexto de empresa relevante (no la memoria personal del owner)
4. Oli muestra los playbooks de equipo disponibles
5. Primera misión: el nuevo miembro hace una misión simple con Oli para entender el flujo
6. Oli actualiza Company Memory: "nuevo miembro [nombre], rol [X], joined [fecha]"
```

---

## Lo que cambia en la arquitectura

### Base de datos

```sql
-- Nueva tabla: teams
CREATE TABLE teams (
    id UUID PRIMARY KEY,
    name TEXT,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMPTZ
);

-- Nueva tabla: team_members
CREATE TABLE team_members (
    team_id UUID REFERENCES teams(id),
    user_id UUID REFERENCES users(id),
    role TEXT,  -- owner | admin | operator | viewer
    joined_at TIMESTAMPTZ,
    PRIMARY KEY (team_id, user_id)
);

-- Misiones ahora tienen team_id y assigned_to
ALTER TABLE missions ADD COLUMN team_id UUID REFERENCES teams(id);
ALTER TABLE missions ADD COLUMN assigned_to UUID REFERENCES users(id);
ALTER TABLE missions ADD COLUMN scope TEXT DEFAULT 'personal';

-- Memoria de empresa es compartida por team_id
ALTER TABLE memory_entries ADD COLUMN team_id UUID REFERENCES teams(id);
-- layer='company' + team_id → compartida con el equipo
-- layer='user' + user_id → privada del miembro
```

### LangGraph — contexto por usuario

Cada misión carga contexto específico del miembro que la ejecuta:

```python
async def retrieve_context_node(state: MissionState) -> MissionState:
    user_id = state["created_by"]
    team_id = state["team_id"]

    context = await memory_graph.recall(MemoryQuery(
        layers=["user"],
        user_id=user_id,       # ← solo la memoria personal del miembro
        min_confidence=0.6
    ))

    team_context = await memory_graph.recall(MemoryQuery(
        layers=["company"],
        team_id=team_id,       # ← memoria compartida del equipo
        min_confidence=0.6
    ))

    return {**state, "context": merge(context, team_context)}
```

---

## Versión de disponibilidad

| Feature | Versión |
|---|---|
| Soporte multi-user básico (roles, permisos) | V1 |
| Memoria personal vs. empresa separada | V1 |
| Asignación de misiones entre miembros | V1 |
| Misiones colaborativas (sub-tareas por miembro) | V2 |
| Playbooks de equipo | V2 |
| Onboarding guiado por Oli para nuevos miembros | V2 |
| Audit trail por miembro (quién aprobó qué) | V1 |
| Roles granulares (más allá de los 4 básicos) | V3+ |

---

## Consecuencias

**Positivo:**
- El trabajo en equipo con IA es un gap real — Oli puede ser el primero en hacerlo bien
- La memoria de empresa compartida hace que todo el equipo trabaje con el mismo contexto
- Los playbooks de equipo multiplican el valor de cada automatización creada

**Negativo:**
- Multi-user agrega complejidad al modelo de datos desde V1
- La gestión de aprobaciones en equipo necesita diseño cuidadoso de UX
- El privacy model es más complejo: ¿qué puede ver cada rol de la memoria de otros?

**Decisión de diseño clave:**
La memoria personal es estrictamente privada — ningún rol, ni siquiera el OWNER,
puede leer la memoria personal de otro miembro. El OWNER puede ver las misiones
ejecutadas por su equipo, pero no las preferencias o correcciones personales.
