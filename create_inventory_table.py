import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('erp_data.db')
cursor = conn.cursor()

# Alte Tabelle löschen (Vorsicht: Alle Daten gehen verloren)
cursor.execute("DROP TABLE IF EXISTS inventory")

# Erstelle die Tabelle 'inventory' mit erweiterten Feldern
cursor.execute('''
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL,
    min_stock INTEGER NOT NULL,
    price REAL NOT NULL,
    manufacturer TEXT NOT NULL,
    supplier TEXT NOT NULL,
    lead_time INTEGER NOT NULL,  -- Lieferzeit in Tagen
    location TEXT NOT NULL,
    weight REAL NOT NULL,  -- Gewicht in Kilogramm
    description TEXT NOT NULL
)
''')

# Beispielhafte Daten einfügen
products = [
    ("Motorbaugruppe", 10000, 500, 2500.00, "AutoTech GmbH", "PartsSupply AG", 14, "Lager Nord", 500.0, "Komplette Motorbaugruppe für verschiedene Fahrzeugmodelle."),
    ("Antriebswelle", 15000, 700, 350.00, "DriveLine Inc.", "FastParts GmbH", 10, "Lager Süd", 20.0, "Verbindet den Motor mit den Rädern und überträgt die Leistung."),
    ("Getriebegehäuse", 20000, 1000, 1500.00, "GearMasters Ltd.", "ProSupply Ltd.", 21, "Lager Ost", 150.0, "Schützt und hält die Getriebekomponenten zusammen."),
    ("Kühlmittelpumpe", 12000, 600, 200.00, "CoolFlow Systems", "AquaParts GmbH", 7, "Lager West", 5.0, "Pumpe zur Zirkulation des Kühlmittels im Motor."),
    ("Zylinderkopf", 18000, 900, 800.00, "CylinderTech", "MotorSupply AG", 15, "Lager Nord", 30.0, "Dichtet den Brennraum ab und beherbergt die Ventile."),
    ("Bremsbeläge", 25000, 1200, 50.00, "BrakeSafe GmbH", "BrakeParts Ltd.", 5, "Lager Süd", 2.5, "Verschleißteile für die Bremsanlage."),
    ("Kupplungsscheibe", 17000, 800, 120.00, "ClutchPro", "DriveParts GmbH", 12, "Lager Ost", 3.0, "Wichtiges Element des Kupplungssystems."),
    ("Turbolader", 16000, 750, 600.00, "TurboBoost Inc.", "SpeedParts AG", 18, "Lager West", 12.0, "Erhöht die Motorleistung durch Verdichtung der Luft."),
    ("Steuergerät", 22000, 1100, 400.00, "ControlTech", "ElectroParts Ltd.", 9, "Lager Nord", 2.0, "Elektronisches Modul zur Steuerung des Motors."),
    ("Schalldämpfer", 14000, 700, 250.00, "SilentDrive", "ExhaustParts GmbH", 14, "Lager Süd", 8.0, "Reduziert die Geräuschentwicklung des Motors."),
    ("Fahrwerksfeder", 13000, 650, 100.00, "SpringWorks", "ChassisParts AG", 11, "Lager Ost", 6.0, "Feder für das Fahrwerk, sorgt für Fahrkomfort."),
    ("Bremssattel", 19000, 950, 180.00, "BrakeMasters", "BrakeSupply GmbH", 10, "Lager West", 4.0, "Komponente der Scheibenbremse, die die Bremsbeläge betätigt."),
    ("Stoßdämpfer", 21000, 1050, 220.00, "ShockAbsorb", "SuspensionParts Ltd.", 13, "Lager Nord", 7.5, "Dämpft die Schwingungen des Fahrwerks."),
    ("Kraftstofffilter", 23000, 1150, 15.00, "FuelClean", "FilterParts GmbH", 4, "Lager Süd", 1.2, "Filtert Verunreinigungen aus dem Kraftstoff."),
    ("Ventildeckel", 11000, 550, 80.00, "ValveCover GmbH", "EngineParts Ltd.", 10, "Lager Ost", 3.5, "Deckel zum Schutz der Ventile im Motor."),
    ("Abgasrückführungsventil", 24000, 1200, 70.00, "EcoExhaust", "EmissionParts AG", 8, "Lager West", 1.8, "Reguliert die Rückführung der Abgase in den Motor."),
    ("Lichtmaschine", 20000, 1000, 300.00, "PowerGen", "ElectroSupply GmbH", 14, "Lager Nord", 6.0, "Erzeugt elektrischen Strom für das Fahrzeug."),
    ("Ölpumpe", 12000, 600, 100.00, "OilFlow Systems", "EngineParts AG", 7, "Lager Süd", 4.0, "Pumpe zur Schmierung der Motorenteile."),
    ("Zündspule", 14000, 700, 60.00, "IgnitePro", "SparkParts GmbH", 6, "Lager Ost", 0.5, "Erzeugt die Zündspannung für die Zündkerzen."),
    ("Riemenscheibe", 9000, 450, 40.00, "BeltDrive", "DriveParts AG", 5, "Lager West", 1.0, "Überträgt die Kraft von der Kurbelwelle auf andere Aggregate."),
    ("Nockenwelle", 16000, 800, 180.00, "Camshaft Inc.", "MotorParts GmbH", 12, "Lager Nord", 5.0, "Steuert die Ventile des Motors."),
    ("Kurbelwelle", 15000, 750, 200.00, "CrankshaftWorks", "EngineSupply Ltd.", 14, "Lager Süd", 25.0, "Verwandelt die Hubbewegung der Kolben in eine Drehbewegung."),
    ("Zylinderblock", 20000, 1000, 1500.00, "BlockMasters", "MotorSupply GmbH", 21, "Lager Ost", 100.0, "Hauptkomponente des Motors, in dem die Zylinder untergebracht sind."),
    ("Kolbenringe", 13000, 650, 20.00, "PistonSeal", "SealParts AG", 7, "Lager West", 0.2, "Dichten den Brennraum gegenüber dem Kurbelgehäuse ab."),
    ("Pleuelstange", 14000, 700, 75.00, "RodTech", "EngineParts Ltd.", 9, "Lager Nord", 3.0, "Verbindet den Kolben mit der Kurbelwelle."),
    ("Ölwannen", 10000, 500, 120.00, "OilPan Inc.", "EngineSupply GmbH", 11, "Lager Süd", 8.0, "Auffangbehälter für das Motoröl."),
    ("Ansaugkrümmer", 17000, 850, 300.00, "IntakeFlow", "AirParts AG", 15, "Lager Ost", 7.0, "Leitet die angesaugte Luft in den Motor."),
    ("Auspuffkrümmer", 13000, 650, 350.00, "ExhaustFlow", "ExhaustParts Ltd.", 16, "Lager West", 10.0, "Leitet die Abgase aus dem Motor in den Auspuff."),
    ("Zahnriemen", 21000, 1050, 50.00, "BeltMasters", "DriveParts GmbH", 4, "Lager Nord", 0.8, "Synchronisiert die Drehbewegung der Kurbel- und Nockenwelle."),
    ("Ventilfeder", 18000, 900, 10.00, "SpringWorks", "ValveParts AG", 3, "Lager Süd", 0.1, "Sorgt dafür, dass das Ventil nach dem Öffnen wieder schließt."),
    ("Drosselklappe", 15000, 750, 200.00, "ThrottleControl", "AirSupply GmbH", 11, "Lager Ost", 2.0, "Reguliert die Luftzufuhr zum Motor."),
    ("Bremsscheibe", 24000, 1200, 80.00, "BrakeDiscs Ltd.", "BrakeParts AG", 8, "Lager West", 4.5, "Bremsscheibe für die Radbremsen."),
    ("Hauptbremszylinder", 12000, 600, 180.00, "MasterBrake", "BrakeSupply GmbH", 10, "Lager Nord", 3.5, "Erzeugt den hydraulischen Druck für die Bremsanlage."),
    ("Hydraulikpumpe", 20000, 1000, 300.00, "HydroPower", "FluidParts Ltd.", 12, "Lager Süd", 15.0, "Pumpe für hydraulische Systeme im Fahrzeug."),
    ("Bremskraftverstärker", 17000, 850, 250.00, "BrakeAssist", "BrakeParts GmbH", 9, "Lager Ost", 5.0, "Verstärkt die Kraft des Fahrers auf das Bremspedal."),
    ("Kraftstoffpumpe", 15000, 750, 100.00, "FuelFlow", "FuelParts AG", 7, "Lager West", 3.0, "Fördert den Kraftstoff vom Tank zum Motor."),
    ("Batterie", 13000, 650, 120.00, "PowerCell", "ElectroSupply GmbH", 5, "Lager Nord", 20.0, "Versorgt das Fahrzeug mit elektrischer Energie."),
    ("Katalysator", 14000, 700, 500.00, "CleanExhaust", "EmissionParts Ltd.", 14, "Lager Süd", 12.0, "Reduziert schädliche Emissionen im Abgas."),
    ("Luftfilter", 22000, 1100, 25.00, "AirClean", "FilterSupply GmbH", 3, "Lager Ost", 0.3, "Filtert Verunreinigungen aus der Luft, bevor sie in den Motor gelangt."),
    ("Ölfilter", 18000, 900, 20.00, "OilClean", "FilterParts AG", 4, "Lager West", 0.5, "Filtert Verunreinigungen aus dem Motoröl."),
    ("Benzinfilter", 11000, 550, 15.00, "FuelClean", "FuelParts GmbH", 4, "Lager Nord", 0.6, "Filtert Verunreinigungen aus dem Kraftstoff."),
    ("Drehzahlgeber", 13000, 650, 60.00, "SpeedSensor", "SensorSupply Ltd.", 6, "Lager Süd", 0.2, "Misst die Drehzahl der Motorwelle."),
    ("Nockenwellensensor", 9000, 450, 70.00, "CamSensor", "MotorSensor GmbH", 7, "Lager Ost", 0.2, "Misst die Position der Nockenwelle."),
    ("Kurbelwellensensor", 12000, 600, 80.00, "CrankSensor", "MotorParts GmbH", 7, "Lager West", 0.3, "Misst die Position der Kurbelwelle."),
    ("Fahrzeugsteuergerät", 16000, 800, 400.00, "CarControl", "ElectroParts GmbH", 10, "Lager Nord", 1.5, "Steuert verschiedene Funktionen des Fahrzeugs."),
    ("Kraftstoffdrucksensor", 14000, 700, 50.00, "FuelSensor", "SensorParts Ltd.", 6, "Lager Süd", 0.2, "Misst den Kraftstoffdruck im System."),
    ("Lambda-Sonde", 20000, 1000, 90.00, "OxygenSensor", "EmissionParts AG", 8, "Lager Ost", 0.4, "Misst den Sauerstoffgehalt im Abgas.")
]

cursor.executemany('''
    INSERT INTO inventory (product_name, stock_quantity, min_stock, price, manufacturer, supplier, lead_time, location, weight, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', products)

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Tabelle 'inventory' wurde zurückgesetzt und mit erweiterten Beispielprodukten gefüllt.")
