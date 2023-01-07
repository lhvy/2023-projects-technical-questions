import express from 'express';
import bodyParser from 'body-parser';

// location is the simple (x, y) coordinates of an entity within the system
// spaceCowboy models a cowboy in our super amazing system
// spaceAnimal models a single animal in our amazing system
type location = { x: number, y: number };
type spaceCowboy = { lassoLength: number, location: location };
type spaceAnimal = { type: "pig" | "cow" | "flying_burger", location: location };


// === ADD YOUR CODE BELOW :D ===

// === ExpressJS setup + Server setup ===
const spaceAnimals = [] as spaceAnimal[];
const spaceCowboys: { [name: string]: spaceCowboy } = {};
const app = express();
app.use(bodyParser.json());

// the POST /entity endpoint adds an entity to your global space database
app.post('/entity', (req, res) => {
  const entities = req.body["entities"];

  for (const entity of entities) {
    const metadata = entity["metadata"];
    const location: location = entity["location"];

    switch (entity["type"]) {
      case "space_cowboy":
        spaceCowboys[metadata["name"]] = { lassoLength: metadata["lassoLength"], location };
        break;

      case "space_animal":
        const type = metadata["type"];
        if (!["pig", "cow", "flying_burger"].includes(type)) {
          res.status(400).send("Invalid Space Animal");
          return;
        }
        spaceAnimals.push({ type, location });
        break;

      default:
        res.status(400).send("Invalid Entity Type");
        return;
    }
  }

  res.status(200).send("OK");
});

// lassoable returns all the space animals a space cowboy can lasso given their name
app.get('/lassoable', (req, res) => {
  const name = req.body["cowboy_name"];

  const cowboy = spaceCowboys[name];
  const space_animals = spaceAnimals.filter(animal => {
    const distance = Math.sqrt(Math.pow(animal.location.x - cowboy.location.x, 2) + Math.pow(animal.location.y - cowboy.location.y, 2));
    return distance <= cowboy.lassoLength;
  });

  res.status(200).send({ space_animals })
});

app.listen(8080);
