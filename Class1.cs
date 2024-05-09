using System.Diagnostics;
using System.Collections.Generic;

public class Class1
{
	static bool[] bools = new bool[] { false, true };

	void Start ()
	{
		char[] chars = new char[1];
		List<string> strings = new List<string>(new string[] { "Hey" });
		// Dictionary<string, int[]> intsDict = new Dictionary<string, int[]>();
		strings.Add("Okiedoke");
		strings.Insert(1, "Howdy");
		for (int i = 0; i < 100; i ++)
		{
			if (i > 50)
				Console.WriteLine("Hello world");
			else
				Console.WriteLine("Hi");
		}
		for (float f = 2; f > -1.5f; f -= .5f)
			Console.WriteLine(strings[0]);
		strings.RemoveAt(0);
		strings.Remove("Howdy");
		PrintAddition (-.1f, 0);
		while (true)
			break;
		do
		{
			string text = @"
Oh no...
!!!!!";
			Console.WriteLine(text.RemoveStartEnd(text.IndexOf(' '), text.LastIndexOf('!')));
			return;
		} while (false);
	}

	static void PrintAddition (float f, float f2)
	{
		Console.Write(f + f2);
	}
}
