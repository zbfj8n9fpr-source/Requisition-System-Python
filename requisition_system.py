from datetime import date

# Global variable for unique requisition ID
requisition_counter = 10000


class Requisition:
    requisitions = []

    def __init__(self, staff_id, staff_name):
        global requisition_counter

        requisition_counter += 1

        self.date = date.today().strftime("%d/%m/%Y")
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.requisition_id = requisition_counter
        self.total = 0
        self.status = "Pending"
        self.approval_reference = "Not available"


    # Add requisition method
    def add_requisition(self, items):

        self.total = sum(items)

        # Automatically approve if below $500
        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = (
                self.staff_id + str(self.requisition_id)
            )

        else:
            self.status = "Pending"

        Requisition.requisitions.append(self)

        return self.total


    # Manager response method
    def respond_requisition(self, response):

        if self.status == "Pending":

            if response.lower() == "approved":
                self.status = "Approved"
                self.approval_reference = (
                    self.staff_id + str(self.requisition_id)
                )

            elif response.lower() == "not approved":
                self.status = "Not approved"


    # Display single requisition
    def display_requisition(self):

        print("---------------------------")
        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: ${self.total}")
        print(f"Status: {self.status}")
        print(
            f"Approval Reference Number: {self.approval_reference}"
        )


    # Display all requisitions
    @classmethod
    def display_all(cls):

        for req in cls.requisitions:
            req.display_requisition()


    # Statistics method
    @classmethod
    def requisition_statistics(cls):

        total = len(cls.requisitions)

        approved = 0
        pending = 0
        not_approved = 0


        for req in cls.requisitions:

            if req.status == "Approved":
                approved += 1

            elif req.status == "Pending":
                pending += 1

            elif req.status == "Not approved":
                not_approved += 1


        print("\nDisplaying the Requisition Statistics")

        print(
            f"\nThe total number of requisitions submitted: {total}"
        )

        print(
            f"The total number of approved requisitions: {approved}"
        )

        print(
            f"The total number of pending requisitions: {pending}"
        )

        print(
            f"The total number of not approved requisitions: {not_approved}"
        )



# -----------------------------
# Testing the program
# -----------------------------


req1 = Requisition("FN19", "John Paul")
req1.add_requisition([100,150,200])


req2 = Requisition("FN20", "Tracy Brown")
req2.add_requisition([400,600])


req3 = Requisition("FN15", "Emma Wellington")
req3.add_requisition([1500,2000])


req4 = Requisition("FN02", "Catlin White")
req4.add_requisition([200,290])


req5 = Requisition("FN25", "David Smith")
req5.add_requisition([800,300])


# Manager responds to pending requests

req2.respond_requisition("Approved")

req3.respond_requisition("Not approved")

req5.respond_requisition("Approved")


# Display results all requisitions and statistics

Requisition.display_all()

Requisition.requisition_statistics()

