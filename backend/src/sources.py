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

SOURCE_LINKS = {
    "capybara_main.txt":                  "https://en.wikipedia.org/wiki/Capybara",
    "capybara_lesser.txt":                "https://en.wikipedia.org/wiki/Lesser_capybara",
    "capybara_genus.txt":                 "https://en.wikipedia.org/wiki/Hydrochoerus",
    "animaldiversity_capybara.txt":       "https://animaldiversity.org/accounts/Hydrochoerus_hydrochaeris/",
    "animaldiversity_hydrochoerinae.txt": "https://animaldiversity.org/accounts/Hydrochoerinae/",
    "britannica_capybara.txt":            "https://www.britannica.com/animal/capybara-genus",
    "nationalgeographic_capybara.txt":    "https://www.nationalgeographic.com/animals/mammals/facts/cabybara-facts",
    "thesprucepets_capybara.txt":         "https://www.thesprucepets.com/capybara-pet-4101211",
    "a-z-animals.txt":                    "https://a-z-animals.com/animals/capybara/",
    "rainforest-alliance.txt":            "https://www.rainforest-alliance.org/species/capybara/",
    "worldwildlife.txt":                  "https://www.worldwildlife.org/resources/facts/are-capybaras-rodents-and-5-other-capybara-facts/",
    "iucn_capybara_redlist.txt":          "https://www.iucnredlist.org/ja/species/10300/22190005#use-trade",
    "habitat_pantanal.txt":               "https://en.wikipedia.org/wiki/Pantanal",
    "habitat_llanos.txt":                 "https://en.wikipedia.org/wiki/Llanos",
    "predator_jaguar.txt":                "https://en.wikipedia.org/wiki/Jaguar",
    "predator_anaconda.txt":              "https://en.wikipedia.org/wiki/Green_anaconda",
    "context_exotic_pet.txt":             "https://en.wikipedia.org/wiki/Exotic_pet",
}


def get_display_name(source_file: str) -> str:
    if source_file in SOURCE_DISPLAY_NAMES:
        return SOURCE_DISPLAY_NAMES[source_file]
    return source_file.replace('.txt', '').replace('_', ' ').title()


def get_link(source_file: str) -> str | None:
    return SOURCE_LINKS.get(source_file)
