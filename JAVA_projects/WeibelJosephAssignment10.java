/*
Name: Joseph Weibel
Class: 2024Sp CS 1450 003
Section: 1
Due: Apr 29, 2024
Description: Assignment #10
This program will create a binary search tree. This program will have to setup the birds in the tree based off their ID number.
This program will then have to compare id numbers to be either before or after other id numbers. The program will store the bird's name
and the phrase of the song they will sing and as the program traverses the binary search tree it will make the birds sing.
*/

import java.io.File;
import java.io.FileNotFoundException;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

 class WeibelJosephAssignment10 {
	//Main method, will hold main logic for the program
	public static void main(String[] args) {
		//Create initial BinaryTree and test binary tree
		BinaryTree binaryTreeTest = new BinaryTree();
		BinaryTree binaryTree = new BinaryTree();
		try {
			//Expects a file object with the argument of the file path to the file to be operated on, will return a scanner object for the file
			Scanner parrotsInfoTest = new Scanner(new File("parrotsTest.txt"));
			
			//hasNextLine takes no arguments and is used to see if there is another line in the file and returns a boolean value
			while(parrotsInfoTest.hasNextLine()) {
				//nextLine returns a Striong of the line being read by the scanner object
				String line = parrotsInfoTest.nextLine();
				//split expects a delimeter as the first argument in String form, and expects an int as the second argument to dictate the amount of indexes to return
				//This will return an array of String objects
				String lineArray[] = line.split(" ", 3);
				//This will take a String as an argument and return a int data type
				int parrotId = Integer.parseInt(lineArray[0]);
				String parrotName = lineArray[1];
				String parrotSong = lineArray[2];
				
				//This is used to create a parrot object and invoke the constructor for the parrot
				//Arguments are in for the id, String for the name, String for the song
				//This will return a String type
				Parrot tempParrot = new Parrot(parrotId, parrotName, parrotSong);
				//This insert method takes a parrot object as an argument and adds it to the binary tree, does not return anything
				binaryTreeTest.insert(tempParrot);
			}
			parrotsInfoTest.close();
		} catch (FileNotFoundException e) {
			System.out.println("Error finding parrots.txt");
		}
		
		System.out.println("Parrot Christmas Song");
		System.out.println("---------------------");
		//visit leaves method will find the parrots in order and print their song piece until there are no more birds
		binaryTreeTest.levelOrder();
		System.out.println("\n");
		System.out.println("Parrots on Leave Nodes");
		System.out.println("----------------------");
		//This method searches the binary tree for nodes that dont have anything attached to left or right and will pring out the node.
		//This does not take arguments and does not return anything
		binaryTreeTest.visitLeaves();
		System.out.println("\n");
		
		
		try {
			//Expects a file object with the argument of the file path to the file to be operated on, will return a scanner object for the file
			Scanner parrotsInfo = new Scanner(new File("parrots.txt"));
			
			//hasNextLine takes no arguments and is used to see if there is another line in the file and returns a boolean value
			while(parrotsInfo.hasNextLine()) {
				//nextLine returns a Striong of the line being read by the scanner object
				String line = parrotsInfo.nextLine();
				//split expects a delimeter as the first argument in String form, and expects an int as the second argument to dictate the amount of indexes to return
				//This will return an array of String objects
				String lineArray[] = line.split(" ", 3);
				//This will take a String as an argument and return a int data type
				int parrotId = Integer.parseInt(lineArray[0]);
				String parrotName = lineArray[1];
				String parrotSong = lineArray[2];
				
				//This is used to create a parrot object and invoke the constructor for the parrot
				//Arguments are in for the id, String for the name, String for the song
				//This will return a String type
				Parrot tempParrot = new Parrot(parrotId, parrotName, parrotSong);
				//This insert method takes a parrot object as an argument and adds it to the binary tree, does not return anything
				binaryTree.insert(tempParrot);
			}
			parrotsInfo.close();
		} catch (FileNotFoundException e) {
			System.out.println("Error finding parrots.txt");
		}
		
		System.out.println("Parrot Christmas Song");
		System.out.println("---------------------");
		//visit leaves method will find the parrots in order and print their song piece until there are no more birds
		binaryTree.levelOrder();
		System.out.println("\n");
		System.out.println("Parrots on Leave Nodes");
		System.out.println("----------------------");
		//This method searches the binary tree for nodes that dont have anything attached to left or right and will pring out the node.
		//This does not take arguments and does not return anything
		binaryTree.visitLeaves();

	}

}
//The purpose of this class is to create parrot objects, these will be used to add to the binary tree
class Parrot{
	private int id;
	private String name;
	private String songPhrase;
	
	//The constructor does not return aynthing, will take int for id, String for name, and STring for song phrase
	public Parrot(int id, String name, String songPhrase) {
		this.id = id;
		this.name = name;
		this.songPhrase = songPhrase;
	}
	//Takes no arguments, returns String for name of object
	public String getName() {
		return this.name;
	}
	//Takes no arguments, returns a String for the song phrase of the Parrot object
	public String sing() {
		return this.songPhrase;
	}
	//Takes a Parrot object as an argument and compares two parrot objects and will return boolean value to see if one ID is tgreater than the other
	public Boolean compareTo(Parrot otherParrot){
		boolean greaterThan = false;
		
		if(this.id > otherParrot.id) {
			greaterThan = false;
		}
		else {
			greaterThan = true;
		}
		return greaterThan;
	}
}
//This class is used to hold the parrot objects in a binary tree
class BinaryTree{
	private TreeNode root;
	//When created the constructor root will be initialized to null
	public BinaryTree(){
		root = null;
	}
	//Takes a parrot as an arguemnt and returns nothing, This miethod has the logic to check if the root is null and make that the parrot
	//If root is not null it will see if the parrot being passed to add is greater than or less than root's id, that will place the parrot
	// On eitehr left or right, if the nodes are not null it will continue checking until it finds a null node in the tree to assign the TreeNode
	public void insert(Parrot parrotToAdd){
		TreeNode newParrot = new TreeNode(parrotToAdd);
		if(root == null) {
			root = newParrot;
		}
		else {
			boolean nullNode = true;
			TreeNode focus = root;
			while(nullNode) {
				//compareTo expects a parrot object as an argument and will return a boolean value it the arguyment id is greater than the focus poarrot
				if(focus.parrot.compareTo(newParrot.parrot)) {
					if(focus.right == null) {
						focus.right = newParrot;
						nullNode = false;
					}
					else {
						focus = focus.right;
					}
				}
				else {
					if(focus.left == null) {
						focus.left = newParrot;
						nullNode = false;
					}
					else {
						focus = focus.left;
					}
				}
			}
		}
	}
	//Level order is used to create a queue and iterate through finding all nodes and using recursion to make all the birds sing their sond
	//This will check the left side first for smaller ids then the right side, adding the TreeNodes to the queue and calling the sing method
	public void levelOrder() {
		Queue<TreeNode> treeQueue = new LinkedList<>();
		//add expects a node as an arguemnt and doesnt return anything, just add something to the queue
		treeQueue.add(root);
		//isEmpty returns a boolean and checks if the queue is empty to continue iterating
		while(!treeQueue.isEmpty()) {
			//remove returns a TreeNode datatype and takes no arguments, will return the one on the bottom of the queue
			TreeNode node = treeQueue.remove();
			System.out.print(node.parrot.sing() + " ");
			
			if(node.left != null) {
				//add expects a node as an arguemnt and doesnt return anything, just add something to the queue
				treeQueue.add(node.left);
			}
			if(node.right != null) {
				//add expects a node as an arguemnt and doesnt return anything, just add something to the queue
				treeQueue.add(node.right);
			}
		}
	}
	//Visit leaves calls the private method visit leaves 
	public void visitLeaves() {
		//Calls private method and expects the root as an argument, does not return anything and will pring out the nodes with null left and right nodes
		visitLeaves(root);
	}
	
	//This method takes a node as an arguiment and will use recursion to find all the nodes with null left and right nodes and print those nodes names
	private void visitLeaves(TreeNode startingNode) {
		if(startingNode != null) {
			if(startingNode.left == null && startingNode.right == null) {
				//uses getter to get the name of trhe node and print
				System.out.println(startingNode.parrot.getName());
			}
			else {
				if(startingNode.left != null) {
					//If both left and right are null check left and call the same method to go deeper into the 
					//binary tree and find one that has null left and right nodes to print out
					visitLeaves(startingNode.left);
				}
				if(startingNode.right != null) {
					//If both left and right are null check right and call the same method to go deeper into the 
					//binary tree and find one that has null left and right nodes to print out
					visitLeaves(startingNode.right);
				}
			}
		}
	}
	
	//This private class is used to create TreeNodes that are used in the binary tree class
	//This is used to create a node and set the left and right of the node to null
	private class TreeNode{
		private Parrot parrot;
		private TreeNode left;
		private TreeNode right;
		
		//The constructor takes a parrot object as an argument and will set the left and right nodes to null
		public TreeNode(Parrot parrot) {
			this.parrot = parrot;
			this.left = null;
			this.right = null;
		}
	}
}