package socialInfluenceObesity;

import repast.simphony.context.Context;
import repast.simphony.dataLoader.ContextBuilder;
import repast.simphony.engine.environment.RunEnvironment;
import repast.simphony.parameter.Parameters;
import repast.simphony.space.graph.Network;
import repast.simphony.context.space.graph.NetworkBuilder;
import repast.simphony.context.space.graph.WattsBetaSmallWorldGenerator;
import org.apache.commons.math3.distribution.GammaDistribution;


/**
 * Social Influence on Obesity Model - World Builder <br>
 * 
 * The InfluenceBuilder creates a world with 100 humans, networked according to 
 * the Watts-Strogatz algorithm. BMIs are initialized according to a gamma distribution. <br>
 * 
 * Humans change their weights at each tick according to their neighbours. <br>
 * 
 * The Environment stops running after 200 ticks. <br>
 * 
 * Environmental parameters to configure the network are defined in parameters.xml
 * and batch_params.xml. This class implements Repast Simphony's Interface ContextBuilder. <br>
 * 
 * @author Ariane Schang 
 *
 */
public class InfluenceBuilder implements ContextBuilder<Human> {
	
	/** 
	 * Builds a context and returns it. This is creating the world according to 
	 * the following specifications: <br> 1) 100 humans with BMIs sampled from 
	 * 15 + a gamma distribution (α=3, β=.25) <br> 2)  Humans connected in a network according to the Watts-Strogatz algorithm with 
	 * degree of 4 and a variable "rewiring probability" 
	 * 
	 * This will build a different Context for each variable parameter combination.
	 * 
	 * @param context An empty context 
	 * @return currentContext The context we've created. 
	 */
	@Override
	public Context<Human> build(Context<Human> context) {
		
		context.setId("Social Influence and Obesity");
		
		
		// Add humans with BMIs initialized according to a right skewed gamma distribution
		// Gamma Distribution takes parameters shape and scale. The shape is the given alpha
		// while the scale is 1/beta. 
		GammaDistribution weightDistr = new GammaDistribution(3, 4);

		for (int i = 0; i < 100; i++) {
			double weight = 15 + weightDistr.sample();			
			context.add(new Human(weight));	
		}
		
		// Get the current run's parameter for the rewiring probability of the network
		Parameters params = RunEnvironment.getInstance().getParameters();
		double rewiringProb = params.getDouble("rewiring_probability");
		
		// Build the network using the Watts Beta Small World Generator
		NetworkBuilder<Human> builder = new NetworkBuilder<Human>("Social Network", context, false);
		builder.setGenerator(new WattsBetaSmallWorldGenerator<Human>(rewiringProb, 4, false));
		Network<Human> net = builder.buildNetwork();
		
		// Set each person's neighbours
		for (Human person: net.getNodes()) {
			Iterable<Human> neighbours = net.getAdjacent(person);
			person.setNeighbours(neighbours);
		}
		
		// End this run after 200 ticks. 
		RunEnvironment.getInstance().endAt(200);
		
		return context;
	}
	

}
