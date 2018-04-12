package socialInfluenceObesity;

import repast.simphony.engine.environment.RunEnvironment;
import repast.simphony.engine.schedule.ScheduledMethod;

/**
 * Social Influence on Obesity Model - Human Class <br>
 * 
 * The Human class contains the attributes relevant to 
 * the people within the model on social influence on obesity.  <br>
 * 
 * Each human has a BMI and a set of neighbours, and when it is their turn,
 * they adjust their BMI according to the average of their neighbours' BMIs. 
 * 
 * @author Ariane Schang
 *
 */
public class Human {
	
	private double bmi;
	private Iterable<Human> neighbours;
	
	/**
	 * Class constructor, creates a human with an initial BMI. 
	 * 
	 * @param bmi Provided when creating the human. 
	 */
	public Human(double bmi) {
		this.bmi = bmi;
	}
	
	/**
	 * Setter method for the human's neighbours. 
	 * Determined by the social network created in the human's context.  
	 * 
	 * @param neighbours Social relations from context. 
	 */
	public void setNeighbours(Iterable<Human> neighbours) {
		this.neighbours = neighbours;
	}
	
	/**
	 * At each tick in the model, all humans (at random) are scheduled to be influenced
	 * by their neighbours and change their weight accordingly. If their neighbours' 
	 * average weight is more than 0.1 away from their own, they move closer to 
	 * the average weight. 
	 * 
	 * As this is the only scheduled method, it does not need to wait or watch any others 
	 * and automatically runs at each tick. 
	 * 
	 */
	@ScheduledMethod(start = 1, interval=1, shuffle = true)
	public void stepWeight() {
		
		/*
		 * Satisficing Radius is a parameter that is changed on each run
		 * Varies discretely between 0.0 and 0.4. 
		 * This radius determines how far of a gap between their own BMI and 
		 * the average BMI can exist before they are willing to make a change.
		*/
		double satisficingRadius = RunEnvironment.getInstance().getParameters().getDouble("satisficing_radius");
		
		// Traverses neighbours to find average weight. 
		double sumWeight = 0;
		double numNeighbours = 0;
		
		for(Human neighbour : neighbours) {
			sumWeight += neighbour.getBmi();
			numNeighbours++;
		}
		
		double avgWeight = sumWeight / numNeighbours;
		 
		double difference = this.bmi - avgWeight;
		
		/*
		 *  Determines whether the difference is large enough to move.
		 *  If so, moves closer to the average.
		 */
		
		if (Math.abs(difference) > satisficingRadius) {
			
			// BMI change doesn't overshoot average.
			if (Math.abs(difference) <= 0.1) {
				this.bmi = avgWeight;
			}
			else if (difference < 0){
				this.bmi += 0.1;
			}
			else if (difference > 0) {
				this.bmi -= 0.1;
			}
		}
		else {
			return;
		}
		
		return;	
	}

	/**
	 * Gets the humans' BMI.
	 * 
	 * @return The BMI.
	 * 
	 */
	public double getBmi() {
		return bmi;
	}
	


}
