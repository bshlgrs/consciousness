/// This sketch of a program illustrates a model of consciousness which
//  would lead someone who used it to believe that inverted spectrum is possible,
//  that Mary learns something when she sees red, and that zombies are
//  conceivable.

// Visual qualia are represented as a triple of numbers--hue, saturation, and
// value. Agents cannot read these numbers directly. These numbers are relative
// to a scale determined by some private feature of the visual system.

// The only way that the agent can introspect on their visual qualia is to
// compare three of them--that is, it can introspect on the relative size of the
// relationships between the pairs (q1, q2) and (q2, q3).

// This restriction means that the agent is able to answer questions about the
// relationship between their qualia without knowing the internal details.

// Furthermore, this means that if a quale from agent 1 were given to agent 2,
// agent 2 could interpret it as a totally different color, because the comparison
// has access to these private features of the quale that instropection does not.
// So this agent thinks that the inverted spectrum would be possible (and probably
// the default assumption about interpersonal qualia comparisons)

// Qualia cannot be constructed by the agent directly, they can only be remembered
// by when you saw them or what their names are. This feature leads to the
// knowledge argument.

// (This bit is more TODO than the other bits) The agent knows that some things
// are agents and some are not. Agents have qualia and nonagents don't. The
// behavior of objects can be predicted by modelling them as agents if they're
// agents (in which case they have qualia) or by modelling them as objects if
// not. Someone with this model of consciousness could be convinced that it's
// possible to build an agent-y-behaving thing out of physical objects, in which
// case they'd assume that it wasn't conscious. (This seems to match what people
// intuitively believe about computer programs.) This sort of matches the standard
// zombie intuition.

// ----

// One major device used in this program is encapsulation via classes. That is,
// the VerbalSystem is only able to call methods on its RestOfBrainInterface,
// as opposed to being able to access the internals of other brain systems directly.
// This means that we can imagine the VerbalSystem being arbitrarily complicated
// but still not able to access any more information than is exposed by that
// interface.

/// ----

// I did not use any of the models of consciousness that we've been discussing
// so far while writing this. I will think about that tomorrow.

/// ---

// I wrote this in Scala rather than Python because I think Scala is better at
// representing encapsulation.

case class VisualQuale(float hue, float saturation, float value)

object VisualQuale {
  // How does the difference between q1 and q2 compare to the difference between q2 and q3?
  // It returns 1 if they're the same. It returns -1 if they're opposite.
  // It returns a larger absolute value than 1 if q1 and q2 are more different than q2 and q3 are.

  // If this is the only method exposed, then the agent will not be able to inspect its internal
  // representations of the qualia.
  def compareHue(q1: VisualQuale, q2: VisualQuale, q3: VisualQuale) = {
    circleDistance(q1.hue, q2.hue) / circleDistance(q2.hue, q3.hue)
  }
}

trait VisualSystem {
  private def look(visualInput: VisualInput)

  def currentQuale: VisualQuale
}

object MathHelper {
  // Takes two numbers and returns the distance of (lhs - rhs) from the largest number
  // which is nonstrictly smaller than it.

  // The invariant is that for all lhs: Float, rhs: Float, lhsMod: Int, rhsMod: Int:
  //     circleDifference(lhs + lhsMod, rhs + rhsMod) == circleDifference(lhs, rhs)
  def circleDifference(lhs: Float, rhs: Float): Float = {
    val difference = lhs - rhs
    Math.floor(difference) - difference
  }
}

trait ConsciousAgent {
  val visualSystem: VisualSystem
  val longTermMemory: LongTermMemory
  val worldModel: WorldModel
  val learningSystem: LearningSystem
  val verbalSystem: VerbalSystem

  def handleNewInput(visualInput: VisualInput) {
    visualSystem.look(visualInput)
    memory.setCurrentQuale(visualSystem.currentQuale)
  }

  def handleInstruction(instruction: String): String {
    verbalSystem.handleInstruction(instruction)
  }
}

// TODO (technical): dependency inject a reference to the VerbalSystemToRestOfBrainInterface
trait VerbalSystem {
  def handleInstruction(string: String): String = {
    // In this function, take instructions like "learn red" and do the specified
    // action, eg learning that the current color is red.

    // The actions are done by calling other methods in this class.
  }

  def compareRememberedQualiaByName(thing1: String, thing2: String, thing3: String): Float = {
    restOfBrainInterface.compareHuesOfRememberedQualiaByNames(thing1, thing2, thing3)
  }

  def askForCurrentLabel {
    restOfBrainInterface.getLabelForCurrentVisualInput()
  }

  def learnLabel(label: String) {
    restOfBrainInterface.learnLabel(label)
  }

  def pictureQualia(label: String) {
    restOfBrainInterface.pictureQualia(label)
  }
}

// TODO (technical): dependency inject a reference to all the other brain components
trait VerbalSystemToRestOfBrainInterface {
  def compareHuesOfRememberedQualiaByNames(thing1: String, thing2: String, thing3: String): Float = {
    val quale1 = memory.getQualeForName(thing1)
    val quale2 = memory.getQualeForName(thing2)
    val quale3 = memory.getQualeForName(thing3)

    VisualQuale.compareHue(quale1, quale2, quale3)
  }

  def getLabelForCurrentVisualInput(): String = {
    val currentQuale = visualInput.currentQuale
    learningSystem.predict(currentQuale)
  }

  def learnLabel(label: String) {
    learningSystem.learn(visualSystem.currentQuale, label)
    memory.rememberLabel(label)
  }

  def pictureQuale(label: String) {
    val quale = memory.getQualeForName(label)
    // You can picture the quale, and it is shown to your Cartesian theater,
    // but no feature of the qualia is available to the rest of the brain.

    // todo: there is no reference to the cartesianTheater anywhere else in this code
    cartesianTheater.show(quale); return ()
  }
}

// Your brain also knows about physical objects, which do things according to
// physical laws.
trait PhysicalObject {
  def mass: Float

  def momentum(velocity: Float) = mass * velocity
}

// This is a creature which uses its mind to learn about colors and
// report on their names.
trait ConsciousHuman extends Agent with PhysicalObject {
  /// ...
}

// This is a creature which uses physical cause and effect to learn about
// colors and report on their names. It does not have qualia.
trait Zombie extends PhysicalObject {
  /// ...
}

