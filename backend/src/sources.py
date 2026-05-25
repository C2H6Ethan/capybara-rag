SOURCE_DISPLAY_NAMES = {
    "capybara_main.txt":                  "Wikipedia — Capybara",
    "capybara_lesser.txt":                "Wikipedia — Lesser Capybara",
    "capybara_genus.txt":                 "Wikipedia — Hydrochoerus",
    "animaldiversity_capybara.txt":       "Animal Diversity Web",
    "animaldiversity_hydrochoerinae.txt": "Animal Diversity Web — Hydrochoerinae",
    "britannica_capybara.txt":            "Encyclopædia Britannica",
    "nationalgeographic_capybara.txt":    "National Geographic",
    "thesprucepets_capybara.txt":         "The Spruce Pets",
    "a-z-animals.txt":                    "A-Z Animals",
    "rainforest-alliance.txt":            "Rainforest Alliance",
    "worldwildlife.txt":                  "World Wildlife Fund",
    "iucn_capybara_redlist.txt":          "IUCN Red List",
    "habitat_pantanal.txt":               "Wikipedia — Pantanal",
    "habitat_llanos.txt":                 "Wikipedia — Llanos",
    "predator_jaguar.txt":                "Wikipedia — Jaguar",
    "predator_anaconda.txt":              "Wikipedia — Green Anaconda",
    "context_exotic_pet.txt":             "Wikipedia — Exotic Pets",
}


def get_display_name(source_file: str) -> str:
    if source_file in SOURCE_DISPLAY_NAMES:
        return SOURCE_DISPLAY_NAMES[source_file]
    return source_file.replace('.txt', '').replace('_', ' ').title()
