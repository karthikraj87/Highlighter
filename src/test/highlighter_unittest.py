import unittest
from main_package.highlighter import highlight_doc

class TestHighlightFunctions(unittest.TestCase):     
    #Basecases
    def test_empty_doc(self):
        doc = ""
        query = "deep dish pizza"
        match = highlight_doc(doc,query)
        print "Test: Empty doc.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match)
  
    def test_blank_doc(self):
        doc = "   "
        query = "deep dish pizza"
        match = highlight_doc(doc,query)
        print "Test: Blank doc i.e doc with only whiteline characters.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match)
  
    def test_empty_query(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = ""
        match = highlight_doc(doc,query)
        print "Test: Empty query.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match)
          
    def test_blank_query(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "   "
        match = highlight_doc(doc,query)
        print "Test: Blank query i.e query with only whiteline characters.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match)
          
    def test_empty_doc_query(self):
        doc = ""
        query = ""
        match = highlight_doc(doc,query)
        print "Test: Empty doc and empty query.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match) 
  
    #Other valid and invalid cases
    def test_full_query_match(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "deep dish pizza"
        match = highlight_doc(doc,query)
        print "Test: Exact match for query in the doc.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("Little star's [[HIGHLIGHT]]deep dish pizza[[ENDHIGHLIGHT]] sure is fantastic.", match)
  
    #Also tests case insensitivity
    def test_singleword_query_match(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "PizZA"
        match = highlight_doc(doc,query)
        print "Test: Exact match for single word query in the doc.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("Little star's deep dish [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]] sure is fantastic.", match)
   
    def test_multiple_singlewords_match(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "funny dogs"
        match = highlight_doc(doc,query)
        print "Test: No exact match found for query but matches found for multiple words in query.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("[[HIGHLIGHT]]Dogs[[ENDHIGHLIGHT]] are [[HIGHLIGHT]]funny[[ENDHIGHLIGHT]]", match)
   
    def test_no_match_multiword_query(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "pita bread"
        match = highlight_doc(doc,query)
        print "Test: None of the words in the multiword query has a match in doc.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match)
   
    def test_no_match_singleword_query(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "bread"
        match = highlight_doc(doc,query)
        print "Test: None of the words in the singleword query has a match in doc.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match)
          
    def test_match_query_long_doc(self):
        doc = """The Chicago-style deep-dish pizza was invented at Pizzeria Uno, in Chicago, in 1943,reportedly by Uno's founder Ike Sewell,
               a former University of Texas football star. However, a 1956 article from the Chicago Daily News asserts that Uno's original
               pizza chef Rudy Malnati developed the recipe. The primary difference between deep-dish pizza and most other forms of pizza
               is that, as the name suggests, the crust is very deep, creating a very thick pizza that resembles a pie more than a flatbread.
               Although the entire pizza is very thick, in traditional Chicago-style deep-dish pizzas, the crust itself is thin to medium in
               thickness, not to be confused with imitations created outside Chicago which use a much thicker crust, often called pan pizza.
               Deep-dish pizza is baked in a round, steel pan that is more similar to a cake or pie pan than a typical pizza pan. The pan is 
               oiled in order to allow for easy removal as well as to create a fried effect on the outside of the crust. In addition to 
               ordinary wheat flour, the pizza dough may contain semolina or food coloring, giving the crust a distinctly yellowish tone. The 
               dough is pressed up onto the sides of the pan, forming a bowl for a very thick layer of toppings. The thick layer of toppings 
               used in deep-dish pizza requires a longer baking time, which could burn cheese or other toppings if they were used as the top 
               layer of the pizza. Because of this, the toppings are assembled 'upside-down' from their usual order on a pizza. The crust is 
               covered with cheese (generally sliced mozzarella), followed by various meat options such as pepperoni or sausage, the latter of 
               which is sometimes in a solid patty-like layer. Other toppings such as onions, mushrooms and bell peppers are then also used. 
               An uncooked sauce, typically made from crushed canned tomatoes, is added as the finishing layer.[1] It is typical that when 
               ordered for carry-out or delivery, that the pizza is uncut, as this prevents the oils from soaking into the crust, causing 
               the pie to become soggy. - Courtesy Wikipedia"""
        query = "pizza"
        match = highlight_doc(doc,query)
        print "Test: Match returns a snippet longer than the default snippet lenght that would be displayed\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("""The Chicago-style deep-dish [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]] was invented at Pizzeria Uno, in Chicago, in 1943,
                           reportedly by Uno's founder Ike Sewell, a former University of Texas football star.However, a 1956 article from 
                           the Chicago Daily News asserts that Uno's original [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]] chef Rudy Malnati developed 
                           the recipe.The primary differen...""", match)  
      
    def test_duplicate_words_in_query_match(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "pizza pizza"
        match = highlight_doc(doc,query)
        print "Test: Duplicate words in query with potential matches in doc.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("Little star's deep dish [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]] sure is fantastic.", match)
      
    def test_duplicate_words_in_query_nomatch(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "pita pita"
        match = highlight_doc(doc,query)
        print "Test: None of the words in the singleword query has a match in doc.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("No matching results found", match)
     
    def test_adjacent_matching_query(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "deep dish"
        match = highlight_doc(doc,query)
        print "Test: Adjacent words in doc match the query.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("Little star's deep dish [[HIGHLIGHT]]pizza pizza[[ENDHIGHLIGHT]] sure is fantastic.", match)
        
    def test_matches_across_multiple_sentences(self):
        doc = "I like fish. Little star's deep dish pizza sure is fantastic. Dogs are funny."
        query = "like pizza"
        match = highlight_doc(doc,query)
        print "Test: Adjacent words in doc match the query.\nDoc: %s\nQuery: %s\nOutput: %s" %(doc, query, match)
        self.assertTrue("Little star's deep dish [[HIGHLIGHT]]pizza pizza[[ENDHIGHLIGHT]] sure is fantastic.", match)

if __name__ == '__main__':
    unittest.main()