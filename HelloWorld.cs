using System.Diagnostics;
using System.Collections.Generic;

public class HelloWorld
{
	public char foo = 'a';
	// List<int> ints = new List<int>() { 1, 2, 3 }; // Fails in CSharpToPythonConverter.cs
	// List<int> ints = [ 1, 2, 3 ]; // Fails in CSharpToPythonConverter.cs
	// public List<int> ints = new List<int>();

	void Start ()
	{
		Console.Write("Hello world");
		Console.Write(foo);
		Test ();
		// ints.Add(1);
		// ints.Add(2);
		// ints.Add(3);
		// foreach (int i in ints)
		// 	Console.Write(i);
	}

	void Test ()
	{
		Console.Write("Hi");
	}
}