from lumina import db
from lumina.models import Users, Projects, Brands, Models, Finishes, Arch_Materials, Material_Types, Floorplan_Shapes, projects_materials
import DBPopulationData

from os import name, path
import sys

def main():

    if not path.exists(r"./lumina/lumina_db.db"):
        db.create_all()
        print("DATABASE CREATED")

    if "populate" in list(map(lambda x : x.lower(), sys.argv)):
        PopulateDatabase()

    if "query" in list(map(lambda x : x.lower(), sys.argv)):

        print(Users.query.all())
        print(Projects.query.all())
        print(Brands.query.all())
        print(Models.query.all())
        print(Finishes.query.all())

def PopulateDatabase():

    # Brands
    for key in DBPopulationData.models:

        brand = Brands(name=key)

        db.session.add(brand)
    db.session.commit()
    brands = Brands.query.all()

    # Material Types
    for name in DBPopulationData.materialTypes:

        materialType = Material_Types(name=name)

        db.session.add(materialType)
    db.session.commit()
    materialTypes = Material_Types.query.all()

    # Finishes
    for name in DBPopulationData.finishes:

        if "metal" in name.lower():
            finish = Finishes(name=name, type_id=list(filter(lambda x : "metal" in x.name.lower(), materialTypes))[0].id)
        
        elif "plastic" in name.lower():
            finish = Finishes(name=name, type_id=list(filter(lambda x : "plastic" in x.name.lower(), materialTypes))[0].id)

        elif "paint" in name.lower():
            finish = Finishes(name=name, type_id=list(filter(lambda x : "paint" in x.name.lower(), materialTypes))[0].id)

        elif "glass" in name.lower():
            finish = Finishes(name=name, type_id=list(filter(lambda x : "glass" in x.name.lower(), materialTypes))[0].id)

        elif "wood" in name.lower():
            finish = Finishes(name=name, type_id=list(filter(lambda x : "wood" in x.name.lower(), materialTypes))[0].id)

        else:
            finish = Finishes(name=name, type_id=list(filter(lambda x : "metal" in x.name.lower(), materialTypes))[0].id)

        db.session.add(finish) 
    db.session.commit()
    finishes = Finishes.query.all()

    # Models
    for brand, model in DBPopulationData.models.items():

        existingModels = Models.query.all()
        existingModels = list(filter(lambda x : x.brand.name == brand, existingModels))
        modelCount = len(existingModels)

        for data in model:

            modelCount = int(modelCount) + 1

            if modelCount < 10:
                modelCount = "0{}".format(modelCount)

            modelForDB = Models(
                name = data["name"],
                productCode = data["productCode"],
                mark = "{}{}".format(brand.upper()[:2], modelCount),
                lm = data["lm"],
                w = data["w"],
                fixtureType = data["fixtureType"],
                length = data["length"],
                width = data["width"],
                height = data["height"],
                diameter = data["diameter"],
                temperature = data["temperature"],
                usage = data["usage"],
                price = data["price"],
                brand_id = list(filter(lambda x : brand == x.name, brands))[0].id,
                finish_id = list(filter(lambda x : data["finish"].lower() == x.name.lower(), finishes))[0].id,
            )

            db.session.add(modelForDB)
        db.session.commit()

    # Floor Plan Shapes
    for shape in DBPopulationData.floorPlanShapes:

        fpShape = Floorplan_Shapes(name=shape)
        db.session.add(fpShape)
    db.session.commit()

    # Architectural Materials
    for name, albedo in DBPopulationData.archMaterials.items():

        if "metal" in name.lower():
            archMaterial = Arch_Materials(name=name, type_id=list(filter(lambda x : "metal" in x.name.lower(), materialTypes))[0].id)
        
        elif "plastic" in name.lower():
            archMaterial = Arch_Materials(name=name, type_id=list(filter(lambda x : "plastic" in x.name.lower(), materialTypes))[0].id)

        elif "paint" in name.lower():
            archMaterial = Arch_Materials(name=name, type_id=list(filter(lambda x : "paint" in x.name.lower(), materialTypes))[0].id)

        elif "glass" in name.lower():
            archMaterial = Arch_Materials(name=name, type_id=list(filter(lambda x : "glass" in x.name.lower(), materialTypes))[0].id)

        elif "wood" in name.lower():
            archMaterial = Arch_Materials(name=name, type_id=list(filter(lambda x : "wood" in x.name.lower(), materialTypes))[0].id)

        else:
            archMaterial = Arch_Materials(name=name, type_id=list(filter(lambda x : "paint" in x.name.lower(), materialTypes))[0].id)

        archMaterial.albedo = albedo
        db.session.add(archMaterial)
    db.session.commit()
   
main()