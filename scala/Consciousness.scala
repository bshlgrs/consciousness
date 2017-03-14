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

// TODO: dependency inject a reference to the VerbalSystemToRestOfBrainInterface
trait VerbalSystem {
  def compareRememberedQualiaByName(thing1: String, thing2: String, thing3: String): Float = {
    restOfBrainInterface.compareHuesOfRememberedQualiaByNames(thing1, thing2, thing3)
  }

  def askForCurrentLabel {
    restOfBrainInterface.getLabelForCurrentVisualInput()
  }

  def learnLabel(label: String) {
    restOfBrainInterface.learnLabel(label)
  }
}

// TODO: dependency inject a reference to all the other brain components
trait VerbalSystemToRestOfBrainInterface {
  def compareHuesOfRememberedQualiaByNames(thing1: String, thing2: String, thing3: String): Float = {
    val quale1 = memory.getQualeForName(thing1)
    val quale2 = memory.getQualeForName(thing2)
    val quale3 = memory.getQualeForName(thing3)

    VisualQuale.compareHue(quale1, quale2, quale3)
  }

  def getLabelForCurrentVisualInput() = {
    val currentQuale = visualInput.currentQuale
    learningSystem.predict(currentQuale)
  }

  def learnLabel(label: String) {
    learningSystem.learn(visualSystem.currentQuale, label)
    memory.rememberLabel(label)
  }
}


trait PhysicalObject {
  def mass: Float

  def momentum(velocity: Float) = mass * velocity
}

trait ConsciousHuman extends Agent with PhysicalObject {

}

trait Zombie extends PhysicalObject {

}

