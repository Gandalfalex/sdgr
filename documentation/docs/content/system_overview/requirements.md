---
title: "Requirements"
date: 2023-12-08T19:22:33+01:00
tags: [RestClient, Django, Spring, Kafka, Redis, Postgres, PostgreSQL, Treafik, Prometheus, Graylog, Hugo]
featured_image: ""
description: "Overview of the System and its communications"
---


{{<mermaid align="left" class="mermaid-large">}}
requirementDiagram

    requirement software {
    id: 1
    text: "Software zur Daten Generierung und Training"
    }

    requirement dataManagement {
    id: 1.1
    text: "Effizientes und flexibles Datenmanagement"
    }

    requirement modelTraining {
    id: 1.2
    text: "Training und Konfiguration von Modellen"
    }

    requirement userInterface {
    id: 1.3
    text: "Benutzerfreundliche Schnittstelle"
    }

    requirement securityPrivacy {
    id: 1.4
    text: "Sicherheit und Datenschutz"
    }

    requirement technical {
    id: 1.5
    text: "Technische Anforderungen für Integration und Deployment"
    }

    software - contains -> dataManagement
    software - contains -> modelTraining
    software - contains -> userInterface
    software - contains -> securityPrivacy
    software - contains -> technical

    requirement versatileDataIntegration {
    id: 1.1.1
    text: "Integration verschiedener Datenquellen und -formate"
    }

    requirement dataProcessing {
    id: 1.1.2
    text: "Verarbeitungslogik für effiziente Datenverarbeitung"
    }

    requirement userFeedback {
    id: 1.1.3
    text: "Visuelles Feedback und Datenexploration"
    }

    dataManagement - contains -> versatileDataIntegration
    dataManagement - contains -> dataProcessing
    dataManagement - contains -> userFeedback

    requirement algorithmSelection {
    id: 1.2.1
    text: "Vielfältige Algorithmenauswahl und Beschreibung"
    }

    requirement modelConfiguration {
    id: 1.2.2
    text: "Intuitive Modellkonfiguration und -anpassung"
    }

    requirement trainingEfficiency {
    id: 1.2.3
    text: "Effiziente Nutzung der Systemressourcen"
    }

    modelTraining - contains -> algorithmSelection
    modelTraining - contains -> modelConfiguration
    modelTraining - contains -> trainingEfficiency

    requirement usabilityPrinciples {
    id: 1.3.1
    text: "Anwendung von Benutzbarkeitsprinzipien (ISO 9241-110)"
    }

    requirement navigation {
    id: 1.3.2
    text: "Klare und verständliche Navigation"
    }

    userInterface - contains -> usabilityPrinciples
    userInterface - contains -> navigation

    requirement dataProtection {
    id: 1.4.1
    text: "DSGVO-konforme Datensicherheit"
    }

    requirement accessControl {
    id: 1.4.2
    text: "Effektive Zugriffskontrollen und Datenisolation"
    }

    securityPrivacy - contains -> dataProtection
    securityPrivacy - contains -> accessControl

    requirement apiIntegration {
    id: 1.5.1
    text: "API-Integration und -Dokumentation"
    }

    requirement errorHandling {
    id: 1.5.2
    text: "Einheitliche Fehlerbehandlung über APIs"
    }

    requirement monitoring {
    id: 1.5.3
    text: "Zentrales Überwachungssystem für Logs und Metriken"
    }

    requirement deploymentStrategy {
    id: 1.5.4
    text: "Durchdachte Deployment-Strategie"
    }

    technical - contains -> apiIntegration
    technical - contains -> errorHandling
    technical - contains -> monitoring
    technical - contains -> deploymentStrategy
{{< /mermaid >}}