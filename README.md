# NUS NextBus API

Some endpoints I got from vibe-reversing the NUS NextBus Android app.
Vibe-coded a helper script to extract credentials from a decompiled `.apk`
file.

NUS please don't expell me 🥺

## GET Endpoints

All follow the pattern:  
`{baseURL}{path}?token={token}{&params}`

| Function Name            | URL Path            | Query Params                          |
|-------------------------|--------------------|---------------------------------------|
| GetListOfBusStops       | BusStops           | (none)                                |
| GetShuttleService       | ShuttleService     | &busstopname={name}                   |
| GetActiveBus            | ActiveBus          | &route_code={code}                    |
| GetPickupPoint          | PickupPoint        | &route_code={code}                    |
| GetBusLocation          | BusLocation        | &veh_plate={encodeURI(plate)}         |
| GetRouteMinMaxTime      | RouteMinMaxTime    | &route_code={code}                    |
| GetServiceDescription   | ServiceDescription | (none)                                |
| GetAnnouncements        | Announcements      | (none)                                |
| GetTickerTapes          | TickerTapes        | (none)                                |
| GetPublicity            | publicity?         | (no token)                            |

---

## Batch GET Endpoints (Promise.all over array)

| Function Name            | URL Path           | Per-item Param         |
|-------------------------|--------------------|------------------------|
| GetAllShuttleServices   | ShuttleService     | &busstopname={name}    |
| GetAllPickuppoints      | PickupPoint        | &route_code={code}     |
| GetAllCheckpoints       | CheckPointBusStop  | &route_code={code}     |

---

## POST Endpoint

| Function Name                | URL Path            | Body      |
|-----------------------------|---------------------|-----------|
| publicityCampaignRegister   | publicity/campaign  | JSON body |

Key Identifiers in the App

- Bus stop: BusstopCode / busstopname
- Route: route_code
- Vehicle: veh_plate
- Polling loops: ActiveBusLoop, ShuttleServiceLoop, AnnouncementsLoop, TickerTapesLoop

---

## Script Usage

1. Obtain the latest version of the NUS NextBus APK
2. Decompile it with `jadx` into a output folder
3. Run `python extract_credentials.py /path/to/output/folder`
