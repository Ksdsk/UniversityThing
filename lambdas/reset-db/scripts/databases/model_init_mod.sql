-- Inserting Schools
INSERT INTO school(school_name) VALUES ("Dalhousie University"), ("McGill University");


-- Inserting Categories for Dalhousie
INSERT INTO category(school_id, category_code, category_name) VALUES 
(1, "ASSC", "Arts and Social Sciences"),
(1, "BIOL", "Biology"),
(1, "BUSI", "Business"),
(1, "CHEM", "Chemistry"),
(1, "COMM", "Commerce"),
(1, "CSCI", "Computer Science"),
(1, "DGIN", "Digital Innovation"),
(1, "ECON", "Economics"),
(1, "ENGL", "English"),
(1, "FILM", "Film Studies"),
(1, "GWST", "Gender and Women's Studies"),
(1, "MGMT", "Management"),
(1, "MATH", "Mathematics"),
(1, "PSYO", "Psychology"),
(1, "STAT", "Statistics"),
(1, "SUST", "Sustainability");
-- Inserting Categories For McGill 
INSERT INTO category(school_id, category_code, category_name) VALUES 
(2, "COMP", "Computer Science"),
(2, "MATH", "Mathematics");


-- Inserting Campus for Dalhousie
INSERT INTO campus(school_id, campus_name) VALUES
(1, "Studley Campus"),
(1, "Sexton Campus"),
(1, "Carleton Campus"),
(1, "Agricultural Campus"),
(1, "Yarmouth Campus"),
(1, "Saint John Campus");
-- Inserting Campus for McGill
INSERT INTO campus(school_id, campus_name) VALUES
(2, "Downtown Campus"),
(2, "Macdonald Campus");
