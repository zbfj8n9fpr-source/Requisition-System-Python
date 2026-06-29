from datetime import date
from typing import Sequence

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
        self.items = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_reference = "Not available"

    def add_requisition(self, items):
        """Add item amounts and calculate the requisition total."""
        try:
            normalized_items = [float(item) for item in items]
        except (TypeError, ValueError) as exc:
            raise ValueError("Items must be a sequence of numeric values.") from exc

        if any(item < 0 for item in normalized_items):
            raise ValueError("Item values cannot be negative.")

        self.items = normalized_items
        self.total = round(sum(normalized_items), 2)

        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = f"{self.staff_id}{self.requisition_id}"
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

        Requisition.requisitions.append(self)
        return self.total

    def respond_requisition(self, response):
        """Approve or reject a pending requisition."""
        if self.status != "Pending":
            return False

        action = response.strip().lower()

        if action in {"approved", "approve"}:
            self.status = "Approved"
            self.approval_reference = f"{self.staff_id}{self.requisition_id}"
        elif action in {"not approved", "not_approved", "reject", "rejected"}:
            self.status = "Not approved"
            self.approval_reference = "Not available"
        else:
            return False

        return True

    def display_requisition(self):
        """Print the requisition details."""
        details = (
            "---------------------------\n"
            f"Date: {self.date}\n"
            f"Requisition ID: {self.requisition_id}\n"
            f"Staff ID: {self.staff_id}\n"
            f"Staff Name: {self.staff_name}\n"
            f"Total: ${self.total:.2f}\n"
            f"Status: {self.status}\n"
            f"Approval Reference Number: {self.approval_reference}"
        )
        print(details)
        return details

    @classmethod
    def display_all(cls):
        """Display every requisition in the system."""
        for req in cls.requisitions:
            req.display_requisition()

    @classmethod
    def requisition_statistics(cls):
        """Generate summary statistics for all requisitions."""
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
        print(f"\nThe total number of requisitions submitted: {total}")
        print(f"The total number of approved requisitions: {approved}")
        print(f"The total number of pending requisitions: {pending}")
        print(f"The total number of not approved requisitions: {not_approved}")

        return {
            "total": total,
            "approved": approved,
            "pending": pending,
            "not_approved": not_approved,
        }


if __name__ == "__main__":
    req1 = Requisition("FN19", "John Paul")
    req1.add_requisition([100, 150, 200])

    req2 = Requisition("FN20", "Tracy Brown")
    req2.add_requisition([400, 600])

    req3 = Requisition("FN15", "Emma Wellington")
    req3.add_requisition([1500, 2000])

    req4 = Requisition("FN02", "Catlin White")
    req4.add_requisition([200, 290])

    req5 = Requisition("FN25", "David Smith")
    req5.add_requisition([800, 300])

    req2.respond_requisition("Approved")
    req3.respond_requisition("Not approved")
    req5.respond_requisition("Approved")

    Requisition.display_all()
    Requisition.requisition_statistics()