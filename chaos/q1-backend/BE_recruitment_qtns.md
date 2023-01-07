1. Identify one problem in the below code block, will this code compile? Discuss the related Rust feature regarding the problem you have identified, why does Rust choose to include this feature? A few sentences are good enough.

   ```rust
       let data = vec![1, 2, 3];
       let my_ref_cell = RefCell::new(69);
       let ref_to_ref_cell = &my_ref_cell;

       std::thread::spawn(move || {

           println!("captured {data:?} by value");

           println!("Whats in the cell?? {ref_to_ref_cell:?}")

       }).join().unwrap();
   ```

   A:

   The error message is

   ```
   the trait `Sync` is not implemented for `RefCell<i32>`
   required because of the requirements on the impl of `Send` for `&RefCell<i32>
   ```

   which indicates that `&RefCell` can't be sent to a thread safely as `Send` is not implemented for it.

   The code will not compile because `RefCell` provides a mutable reference to a value. The thread has been given an immutable reference to the `RefCell` but is still able to mutate the underlying value the `RefCell` contains, which could cause a data race.

   The related Rust feature is Send (indicates ownership of values can be transferred across threads) and Sync (indicates references to a type are safe across threads). For type `T` to implement `Sync`, `&T` must implement `Send`, meaning it can safely cross thread boundaries. This is a useful feature because two simple traits can now be used to enforce data race safety across threads.

2. Shortly discuss, when modelling a response to a HTTP request in Rust, would you prefer to use `Option` or `Result`?

   A: Result because HTTP responses can be successful (i.e. 200 OK) or unsuccessful (i.e. 404 Not Found). Success codes can be represented by `Ok` and failure codes are represented by `Err`. Option is not suitable because it only represents the presence or absence of a value, no information about the success or failure of the operation.

3. In `student.psv` there are some fake student datas from UNSW CSE (no doxx!). In each row, the fields from left to right are

   - UNSW Course Code
   - UNSW Student Number
   - Name
   - UNSW Program
   - UNSW Plan
   - WAM
   - UNSW Session
   - Birthdate
   - Sex

   Write a Rust program to find the course which has the highest average student WAM. **Write your program in the cargo project q3**.
