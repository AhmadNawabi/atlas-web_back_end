-- Trigger to decrease item quantity on new order
DELIMITER //

CREATE TRIGGER after_order_decrease
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
//

DELIMITER ;
