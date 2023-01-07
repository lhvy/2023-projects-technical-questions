// q3
// In `student.psv` there are some fake student datas from UNSW CSE (no doxx!). In each row, the fields from left to right are
//
// - UNSW Course Code
// - UNSW Student Number
// - Name
// - UNSW Program
// - UNSW Plan
// - WAM
// - UNSW Session
// - Birthdate
// - Sex
//
// Write a Rust program to find the course which has the highest average student WAM.

use std::cell::RefCell;
use std::collections::HashMap;

// Sample input: COMP4963|5555555|Student, Fake |9999/1|FAKEAA|099.99|22T2|20000122|F
struct Mark<'a> {
    course_code: &'a str,
    wam: f32,
}

#[derive(Default)]
struct Course {
    avg_wam: f32,
    // Store count for rolling average
    count: u32,
}

fn main() {
    let data = vec![1, 2, 3];
    let my_ref_cell = RefCell::new(69);
    let ref_to_ref_cell = &my_ref_cell;

    std::thread::spawn(move || {
        println!("captured {data:?} by value");

        println!("Whats in the cell?? {ref_to_ref_cell:?}")
    })
    .join()
    .unwrap();

    // Read student.psv from ../student.psv
    let mut marks = Vec::new();
    let file = std::fs::read_to_string("../student.psv").unwrap();

    // Parse each line into a Mark struct
    for line in file.lines() {
        let mut fields = line.split('|');
        let mark = Mark {
            course_code: fields.next().unwrap(),
            // WAM is at index 5 but we can't use nth(5) because we already used next()
            wam: fields.nth(4).unwrap().parse().unwrap(),
        };
        marks.push(mark);
    }

    // Find the course with the highest average WAM
    let mut courses: HashMap<&str, Course> = HashMap::with_capacity(marks.len());
    for mark in marks {
        let course = courses.entry(mark.course_code).or_default();
        // Calculate rolling average
        course.avg_wam =
            (course.avg_wam * course.count as f32 + mark.wam) / (course.count + 1) as f32;
        course.count += 1;
    }

    // Find the course with the highest average WAM
    let mut wam = 0.0;
    let mut course_code = "No course";
    for (code, course) in courses {
        if course.avg_wam > wam {
            wam = course.avg_wam;
            course_code = code;
        }
    }
    println!("Course with highest average WAM: {course_code} ({wam})");
}
